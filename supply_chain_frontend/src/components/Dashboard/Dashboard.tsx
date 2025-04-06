import React from 'react';
import { 
  LayoutDashboard, 
  Truck, 
  TrendingUp, 
  Warehouse, 
  PackageCheck, 
  BarChart3, 
  Settings, 
  Search, 
  HelpCircle, 
  User,
  AlertTriangle
} from 'lucide-react';
import SupplyChainChart from './SupplyChainChart';
import ShipmentMap from './ShipmentMap';

const Dashboard: React.FC = () => {
  return (
    <div className="flex min-h-screen bg-[#f8f9fa]">
      {/* Sidebar */}
      <div className="w-[224px] bg-[#0f172a] text-white flex flex-col">
        <div className="p-6 border-b border-[#1e293b] mb-4">
          <h1 className="text-xl font-bold">AI Supply Chain</h1>
        </div>
        
        <div className="flex flex-col space-y-1 px-2">
          <SidebarItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
          <SidebarItem icon={<Truck size={20} />} label="Live Shipments" />
          <SidebarItem icon={<TrendingUp size={20} />} label="AI Predictions" />
          <SidebarItem icon={<Warehouse size={20} />} label="Warehouses" />
          <SidebarItem icon={<PackageCheck size={20} />} label="Orders & Inventory" />
          <SidebarItem icon={<BarChart3 size={20} />} label="Reports" />
          <SidebarItem icon={<Settings size={20} />} label="Settings" />
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div className="relative w-[300px]">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
            <input 
              type="text" 
              placeholder="Search" 
              className="pl-10 pr-4 py-2 bg-[#f1f5f9] rounded-full w-full text-sm focus:outline-none"
            />
          </div>
          <div className="flex items-center space-x-4">
            <button className="p-2 rounded-full bg-[#f1f5f9]">
              <HelpCircle size={20} className="text-[#1e293b]" />
            </button>
            <button className="p-2 rounded-full bg-[#1e293b]">
              <User size={20} className="text-white" />
            </button>
          </div>
        </div>
        
        {/* Main Grid */}
        <div className="grid grid-cols-2 gap-6 mb-6">
          {/* Current Demand Forecast */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-medium mb-4">Current Demand Forecast</h2>
            <div className="flex flex-col">
              <span className="text-5xl font-bold mb-2">7,500</span>
              <span className="text-sm text-gray-600">95% AI prediction confidence</span>
            </div>
          </div>
          
          {/* System Health */}
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-lg font-medium mb-4">System Health</h2>
            <div className="flex items-center">
              <div className="w-4 h-4 rounded-full bg-emerald-500 mr-3"></div>
              <span className="text-xl font-medium">Healthy</span>
            </div>
          </div>
        </div>
        
        {/* Secondary Grid */}
        <div className="grid grid-cols-4 gap-6 mb-6">
          {/* Shipments in Transit */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="mb-2">
              <ShipmentMap />
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-medium text-gray-700">Shipments</span>
              <span className="text-sm font-medium text-gray-700">In Transit</span>
              <span className="text-2xl font-bold mt-1">28</span>
            </div>
          </div>
          
          {/* Average Delivery Time */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Average Delivery Time</h3>
            <div className="flex flex-col">
              <span className="text-3xl font-bold">2.5</span>
              <span className="text-xl font-medium">days</span>
            </div>
          </div>
          
          {/* Stock Availability */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Stock Availability</h3>
            <div className="flex flex-col">
              <span className="text-3xl font-bold mb-2">92 <span className="text-xl">%</span></span>
              <div className="space-y-1">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-emerald-500 mr-2"></div>
                  <span className="text-xs text-gray-600">Warehouse</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-emerald-500 mr-2"></div>
                  <span className="text-xs text-gray-600">Route opti.zen</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Delay Risk Forecast */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Delay Risk Forecast</h3>
            <div className="flex items-center mb-2">
              <AlertTriangle size={24} className="text-gray-700 mr-2" />
              <span className="text-2xl font-bold">Low</span>
            </div>
          </div>
        </div>
        
        {/* Chart Section */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <h2 className="text-lg font-medium mb-4">Demand Forecast vs. Actual and Optimization Effectiveness</h2>
          <div className="h-64">
            <SupplyChainChart />
          </div>
        </div>
      </div>
    </div>
  );
};

// Sidebar Item Component
const SidebarItem = ({ icon, label, active = false }) => (
  <div className={`flex items-center py-2 px-3 rounded-md cursor-pointer ${active ? 'bg-[#1e293b] font-medium' : 'hover:bg-[#1e293b] text-gray-300'}`}>
    <div className="mr-3">{icon}</div>
    <span>{label}</span>
  </div>
);

export default Dashboard;