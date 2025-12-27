import React from 'react';

interface SuccessMessageProps {
  message: string;
  className?: string;
  onDismiss?: () => void;
}

export const SuccessMessage: React.FC<SuccessMessageProps> = ({
  message,
  className = '',
  onDismiss,
}) => {
  return (
    <div
      className={`bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded relative ${className}`}
      role="alert"
    >
      <span className="block sm:inline">{message}</span>
      {onDismiss && (
        <button
          className="absolute top-0 bottom-0 right-0 px-4 py-3"
          onClick={onDismiss}
          aria-label="Dismiss success message"
        >
          <span className="text-green-700 hover:text-green-900">×</span>
        </button>
      )}
    </div>
  );
};

