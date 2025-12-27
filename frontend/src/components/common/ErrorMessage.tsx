import React from 'react';

interface ErrorMessageProps {
  message: string;
  className?: string;
  onDismiss?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  className = '',
  onDismiss,
}) => {
  return (
    <div
      className={`bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative ${className}`}
      role="alert"
    >
      <span className="block sm:inline">{message}</span>
      {onDismiss && (
        <button
          className="absolute top-0 bottom-0 right-0 px-4 py-3"
          onClick={onDismiss}
          aria-label="Dismiss error"
        >
          <span className="text-red-700 hover:text-red-900">×</span>
        </button>
      )}
    </div>
  );
};

