import React from 'react';
import { Link } from 'react-router-dom';
const Navbar = () => {
  return (
    <nav className="flex items-center justify-between px-12 py-4 bg-background text-foreground">
      <div className="flex items-center space-x-2">
        <span className="text-4xl font-bold text-primary">AuraLens AI</span>
      </div>
      <div className="flex items-center space-x-6">
        <Link to="/" className="text-lg hover:text-secondary transition-colors duration-200">Home</Link>
        <Link to="/about" className="text-lg hover:text-secondary transition-colors duration-200">About</Link>
        <Link to="/contact" className="text-lg hover:text-secondary transition-colors duration-200">Contact</Link>
      </div>
    </nav>
  );
};

export default Navbar;
