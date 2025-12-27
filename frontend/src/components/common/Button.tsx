'use client';

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export default function Button({ variant = 'primary', children, className, ...props }: ButtonProps) {
  const baseStyles = {
    marginTop: '1rem',
    display: 'inline-block',
    padding: '0.8rem 3rem',
    fontSize: '1.7rem',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    textAlign: 'center' as const,
    border: '0.2rem solid',
  };

  const variantStyles = {
    primary: {
      background: 'var(--orange)',
      color: '#fff',
      borderColor: 'var(--orange)',
    },
    secondary: {
      background: 'none',
      color: 'var(--black)',
      borderColor: 'var(--black)',
    },
  };

  return (
    <button
      className={`btn ${className || ''}`}
      style={{ ...baseStyles, ...variantStyles[variant] }}
      {...props}
    >
      {children}
    </button>
  );
}

