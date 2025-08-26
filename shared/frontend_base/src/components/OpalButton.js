import React from 'react';
import { Button } from 'react-bootstrap';
import '../styles/main.css'; // Import custom styles

const OpalButton = ({ children, ...props }) => {
  return (
    <Button className="opal-button" {...props}>
      {children}
    </Button>
  );
};

export default OpalButton;