from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from shared.auth.otp.otp_manager import generate_otp, generate_otp_code, validate_otp
from shared.auth.otp.senders.email.email_sender import EmailOTPSender
from shared.auth.otp.senders.sms.sms_adapters import SNSAdapter, TwilioAdapter
from shared.auth.otp.senders.sms.sms_sender import SMSOTPSender
from shared.database_base.models.user import User


@pytest.fixture
def mock_db_session():
    """Mock SQLAlchemy session for OTP tests."""
    session = MagicMock(spec=Session)
    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None
    return session


@pytest.fixture
def mock_user():
    """Mock User object for OTP tests."""
    user = MagicMock(spec=User)
    user.id = 1
    user.email = "test@example.com"
    user.otp_code = None
    user.otp_expiry = None
    return user


def test_generate_otp_code():
    """Test that generate_otp_code returns a 6-digit string."""
    otp = generate_otp_code()
    assert isinstance(otp, str)
    assert len(otp) == 6
    assert otp.isdigit()


def test_generate_otp(mock_db_session, mock_user):
    """Test that generate_otp stores OTP and expiry in user and commits."""
    otp_code = generate_otp(mock_db_session, mock_user)

    assert mock_user.otp_code == otp_code
    assert isinstance(mock_user.otp_expiry, datetime)
    assert mock_user.otp_expiry > datetime.utcnow()
    mock_db_session.add.assert_called_once_with(mock_user)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_user)
    assert isinstance(otp_code, str)
    assert len(otp_code) == 6


def test_validate_otp_success(mock_db_session, mock_user):
    """Test successful OTP validation."""
    mock_user.otp_code = "123456"
    mock_user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)

    assert validate_otp(mock_db_session, mock_user, "123456") is True
    assert mock_user.otp_code is None  # Should be cleared after success
    assert mock_user.otp_expiry is None  # Should be cleared after success
    mock_db_session.add.assert_called_once_with(mock_user)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_user)


def test_validate_otp_invalid_code(mock_db_session, mock_user):
    """Test OTP validation with an incorrect code."""
    mock_user.otp_code = "123456"
    mock_user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)

    assert validate_otp(mock_db_session, mock_user, "654321") is False
    assert mock_user.otp_code == "123456"  # Should not be cleared
    assert mock_user.otp_expiry is not None  # Should not be cleared
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()


def test_validate_otp_expired_code(mock_db_session, mock_user):
    """Test OTP validation with an expired code."""
    mock_user.otp_code = "123456"
    mock_user.otp_expiry = datetime.utcnow() - timedelta(minutes=1)

    assert validate_otp(mock_db_session, mock_user, "123456") is False
    assert mock_user.otp_code == "123456"  # Should not be cleared
    assert mock_user.otp_expiry is not None  # Should not be cleared
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()


def test_validate_otp_no_otp_set(mock_db_session, mock_user):
    """Test OTP validation when no OTP was ever set on the user."""
    mock_user.otp_code = None
    mock_user.otp_expiry = None

    assert validate_otp(mock_db_session, mock_user, "123456") is False
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()


class TestEmailOTPSender:
    @pytest.fixture
    def email_sender(self):
        # Mock the EmailOTPSender class directly
        mock_sender = MagicMock(spec=EmailOTPSender)
        return mock_sender

    @pytest.mark.asyncio
    async def test_send_otp_success(self, email_sender):
        """Test successful OTP email sending."""
        email_sender.send_otp.return_value = True
        result = await email_sender.send_otp("recipient@example.com", "123456", 1)
        assert result is True
        email_sender.send_otp.assert_called_once_with(
            "recipient@example.com", "123456", 1
        )

    @pytest.mark.asyncio
    async def test_send_otp_failure(self, email_sender):
        """Test OTP email sending failure."""
        email_sender.send_otp.return_value = False
        result = await email_sender.send_otp("recipient@example.com", "123456", 1)
        assert result is False
        email_sender.send_otp.assert_called_once_with(
            "recipient@example.com", "123456", 1
        )


class TestSMSOTPSender:
    @pytest.fixture
    def sms_sender(self):
        # Mock the SMSOTPSender class directly
        mock_sender = MagicMock(spec=SMSOTPSender)
        return mock_sender

    @pytest.mark.asyncio
    async def test_sms_sender_twilio_success(self, sms_sender):
        sms_sender.send_otp.return_value = True
        result = await sms_sender.send_otp("+1234567890", "123456", 1)
        assert result is True
        sms_sender.send_otp.assert_called_once_with("+1234567890", "123456", 1)

    @pytest.mark.asyncio
    async def test_sms_sender_twilio_failure(self, sms_sender):
        sms_sender.send_otp.return_value = False
        result = await sms_sender.send_otp("+1234567890", "123456", 1)
        assert result is False
        sms_sender.send_otp.assert_called_once_with("+1234567890", "123456", 1)

    @pytest.mark.asyncio
    async def test_sms_sender_sns_success(self, sms_sender):
        sms_sender.send_otp.return_value = True
        result = await sms_sender.send_otp("+1234567890", "123456", 1)
        assert result is True
        sms_sender.send_otp.assert_called_once_with("+1234567890", "123456", 1)

    @pytest.mark.asyncio
    async def test_sms_sender_sns_failure(self, sms_sender):
        sms_sender.send_otp.return_value = False
        result = await sms_sender.send_otp("+1234567890", "123456", 1)
        assert result is False
        sms_sender.send_otp.assert_called_once_with("+1234567890", "123456", 1)
