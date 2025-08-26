import ast
import os
import sys


def find_files(root_dir, extensions):
    """Recursively finds files with given extensions, ignoring common dev directories."""
    found_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip directories
        dirnames[:] = [
            d
            for d in dirnames
            if d not in [".git", ".venv", "node_modules", "__pycache__"]
            and not d.startswith(".")
        ]
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                found_files.append(os.path.join(dirpath, filename))
    return found_files


def check_for_direct_redis_imports():
    """Checks for direct imports of the 'redis' library in the auth_service."""
    violations = []
    auth_service_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "auth_service")
    )
    allowed_redis_import = os.path.join(
        auth_service_root, "adapters", "redis_otp_store.py"
    )

    for subdir, _, files in os.walk(auth_service_root):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(subdir, file)
                if file_path == allowed_redis_import:
                    continue

                with open(file_path, "r") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import) and any(
                                alias.name == "redis" for alias in node.names
                            ):
                                violations.append(
                                    f"Violation in {file_path}: Direct 'redis' import found. Please use the OTP store interface."
                                )
                            elif (
                                isinstance(node, ast.ImportFrom)
                                and node.module == "redis"
                            ):
                                violations.append(
                                    f"Violation in {file_path}: Direct 'from redis import ...' found. Please use the OTP store interface."
                                )
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")
    return violations


def check_architecture():
    """Enforces architecture rules for the monorepo."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    violations = []

    # --- Authentication Module Check ---
    auth_modules = []
    central_auth_path = os.path.join(repo_root, "shared", "common", "auth")

    # Known exceptions for authentication modules (to be refactored later)
    AUTH_EXCEPTIONS = [
        "MonitorIQ/auth",
    ]

    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Skip ignored directories
        if any(
            ignored_dir in dirpath
            for ignored_dir in [
                os.sep + ".git" + os.sep,
                os.sep + ".venv" + os.sep,
                os.sep + "venv" + os.sep,
                os.sep + "node_modules" + os.sep,
                os.sep + "__pycache__" + os.sep,
            ]
        ) or os.path.basename(dirpath).startswith("."):
            continue

        # Skip shared/common/auth itself
        if os.path.abspath(dirpath) == central_auth_path:
            continue

        # Look for directories named 'auth' or 'authentication' containing Python files
        if os.path.basename(dirpath).lower() in ["auth", "authentication"]:
            if any(f.endswith(".py") for f in filenames):
                auth_modules.append(os.path.relpath(dirpath, repo_root))

    # Filter out known exceptions
    auth_modules = [m for m in auth_modules if m not in AUTH_EXCEPTIONS]

    if len(auth_modules) > 0:
        violations.append(
            "Architecture Violation: Found unauthorized authentication modules outside 'shared/common/auth/'."
        )
        for module in auth_modules:
            violations.append(f"- {module}")

    # --- UI/CSS Control Module Check ---
    ui_css_modules = []
    central_ui_path = os.path.join(repo_root, "shared", "frontend_base")

    # Known exceptions for UI/CSS control modules (to be refactored later)
    UI_CSS_EXCEPTIONS = [
        "RegressionInsight/src/webapp/frontend/src/UI/Global/styles",
    ]

    # Extensions to look for in UI/CSS directories
    ui_css_extensions = (".js", ".jsx", ".ts", ".tsx", ".css", ".scss", ".less")

    for dirpath, dirnames, filenames in os.walk(repo_root):
        # Skip ignored directories and build directories
        if any(
            ignored_dir in dirpath
            for ignored_dir in [
                os.sep + ".git" + os.sep,
                os.sep + ".venv" + os.sep,
                os.sep + "venv" + os.sep,
                os.sep + "node_modules" + os.sep,
                os.sep + "__pycache__" + os.sep,
                os.sep + "build" + os.sep,  # Ignore build directories
            ]
        ) or os.path.basename(dirpath).startswith("."):
            continue

        # If the current directory is the central UI path or a subdirectory of it, skip it
        if (
            os.path.abspath(dirpath).startswith(central_ui_path)
            and os.path.abspath(dirpath) != central_ui_path
        ):
            continue

        # Look for directories named 'ui', 'frontend', 'theme', 'styles', 'css'
        # that contain relevant UI/CSS files
        if os.path.basename(dirpath).lower() in [
            "ui",
            "frontend",
            "theme",
            "styles",
            "css",
        ]:
            if any(f.endswith(ext) for f in filenames for ext in ui_css_extensions):
                ui_css_modules.append(os.path.relpath(dirpath, repo_root))

    # Filter out known exceptions
    ui_css_modules = [m for m in ui_css_modules if m not in UI_CSS_EXCEPTIONS]

    if len(ui_css_modules) > 0:
        violations.append(
            "Architecture Violation: Found unauthorized UI/CSS control modules outside 'shared/frontend_base/'."
        )
        for module in ui_css_modules:
            violations.append(f"- {module}")

    # --- Redis Import Check ---
    violations.extend(check_for_direct_redis_imports())

    if violations:
        print("\n--- Architectural Violations Found! ---")
        for violation in violations:
            print(f"- {violation}")
        print(
            "\nPlease correct these violations to maintain architectural consistency."
        )
        sys.exit(1)
    else:
        print("\n--- All architectural checks passed! ---")
        sys.exit(0)


if __name__ == "__main__":
    check_architecture()
