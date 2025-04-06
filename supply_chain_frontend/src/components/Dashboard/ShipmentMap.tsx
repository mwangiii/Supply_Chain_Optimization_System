import React from 'react';

const ShipmentMap: React.FC = () => {
  return (
    <div className="w-full h-[100px] relative bg-gray-100 rounded-md">
      {/* This is a simple map visualization, in a real app you'd use a map library */}
      <div className="absolute inset-0 flex items-center justify-center">
        <svg width="100%" height="100%" viewBox="0 0 200 100" fill="none">
          <path
            d="M40,60 Q70,30 100,50 T160,60"
            stroke="#3b82f6"
            strokeWidth="3"
            fill="none"
          />
          <circle cx="40" cy="60" r="5" fill="#3b82f6" />
          <circle cx="160" cy="60" r="5" fill="#1e293b" stroke="#ffffff" strokeWidth="2" />
        </svg>
      </div>
    </div>
  );
};

export default ShipmentMap;