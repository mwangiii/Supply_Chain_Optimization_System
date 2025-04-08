import React, { useState, useEffect } from 'react';
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
  AlertTriangle,
  Loader
} from 'lucide-react';
import SupplyChainChart from './SupplyChainChart';
import ShipmentMap from './ShipmentMap';
import Tracking from './Tracking';
import AiPredictions from './AiPredictions';

const Dashboard: React.FC = () => {
  const [demandForecast, setDemandForecast] = useState<number | null>(null);
  const [forecastConfidence, setForecastConfidence] = useState<number | null>(null);
  const [systemHealth, setSystemHealth] = useState('Loading');
  const [shipmentsInTransit, setShipmentsInTransit] = useState<number | null>(null);
  const [averageDeliveryTime, setAverageDeliveryTime] = useState<number | null>(null);
  const [stockAvailability, setStockAvailability] = useState<number | null>(null);
  const [delayRisk, setDelayRisk] = useState('Loading');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('Dashboard');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        const forecastResponse = await fetch(`${import.meta.env.VITE_BASE_API_URL}/forecast/demand`);
        if (!forecastResponse.ok) throw new Error('Failed to fetch demand forecast data');
        const forecastData = await forecastResponse.json();
        
        const trendsResponse = await fetch(`${import.meta.env.VITE_BASE_API_URL}/forecast/trends`);
        if (!trendsResponse.ok) throw new Error('Failed to fetch trends data');
        const trendsData = await trendsResponse.json();
        
        const modelStatusResponse = await fetch(`${import.meta.env.VITE_BASE_API_URL}/forecast/model/status`);
        if (!modelStatusResponse.ok) throw new Error('Failed to fetch model status');
        const modelStatusData = await modelStatusResponse.json();

        setDemandForecast(forecastData.forecast_value || 0);
        setForecastConfidence(forecastData.confidence || 0);
        setSystemHealth(modelStatusData.health_status || 'Unknown');
        setShipmentsInTransit(trendsData.shipments_in_transit || 0);
        setAverageDeliveryTime(trendsData.avg_delivery_time || 0);
        setStockAvailability(trendsData.stock_availability || 0);
        setDelayRisk(trendsData.delay_risk || 'Unknown');
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again later.');
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const getStatusColor = (status: string) => {
    switch(status?.toLowerCase()) {
      case 'healthy':
      case 'good':
      case 'low':
        return 'bg-emerald-500';
      case 'warning':
      case 'medium':
        return 'bg-amber-500';
      case 'error':
      case 'critical':
      case 'high':
        return 'bg-red-500';
      default:
        return 'bg-gray-400';
    }
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex justify-center items-center h-64">
          <Loader size={48} className="animate-spin text-blue-500" />
        </div>
      );
    }

    switch (activeTab) {
      case 'Dashboard':
        return (
          <>
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                <p>{error}</p>
              </div>
            )}
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h2 className="text-lg font-medium mb-4">Current Demand Forecast</h2>
                <div className="flex flex-col">
                  <span className="text-5xl font-bold mb-2">{demandForecast?.toLocaleString() || 'N/A'}</span>
                  <span className="text-sm text-gray-600">{forecastConfidence}% AI prediction confidence</span>
                </div>
              </div>
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h2 className="text-lg font-medium mb-4">System Health</h2>
                <div className="flex items-center">
                  <div className={`w-4 h-4 rounded-full ${getStatusColor(systemHealth)} mr-3`} />
                  <span className="text-xl font-medium">{systemHealth}</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-4 gap-6 mb-6">
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="mb-2">
                  <ShipmentMap />
                </div>
                <div className="flex flex-col">
                  <span className="text-sm font-medium text-gray-700">Shipments</span>
                  <span className="text-sm font-medium text-gray-700">In Transit</span>
                  <span className="text-2xl font-bold mt-1">{shipmentsInTransit || 'N/A'}</span>
                </div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Average Delivery Time</h3>
                <div className="flex flex-col">
                  <span className="text-3xl font-bold">{averageDeliveryTime || 'N/A'}</span>
                  <span className="text-xl font-medium">days</span>
                </div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Stock Availability</h3>
                <div className="flex flex-col">
                  <span className="text-3xl font-bold mb-2">{stockAvailability || 'N/A'}%</span>
                  <div className="space-y-1">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-emerald-500 mr-2" />
                      <span className="text-xs text-gray-600">Warehouse</span>
                    </div>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-emerald-500 mr-2" />
                      <span className="text-xs text-gray-600">Route optimization</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Delay Risk Forecast</h3>
                <div className="flex items-center mb-2">
                  <AlertTriangle 
                    size={24} 
                    className={`mr-2 ${
                      delayRisk?.toLowerCase() === 'high' ? 'text-red-500' :
                      delayRisk?.toLowerCase() === 'medium' ? 'text-amber-500' :
                      'text-gray-700'
                    }`} 
                  />
                  <span className="text-2xl font-bold">{delayRisk}</span>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h2 className="text-lg font-medium mb-4">Demand Forecast vs. Actual and Optimization Effectiveness</h2>
              <div className="h-64">
                <SupplyChainChart />
              </div>
            </div>
          </>
        );
      case 'Live Shipments':
        return (
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <Tracking /> {/* Render the Tracking component */}
          </div>
        );
      case 'AI Predictions': // Add case for AI Predictions
        return (
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <AiPredictions modelId="defaultModelId" />
          </div>
        );
      case 'Orders & Inventory':
        return (
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <Tracking /> {/* Render the Tracking component */}
          </div>
        );
      default:
        return (
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-xl font-semibold mb-2">{activeTab}</h2>
            <p>This is the {activeTab} content section. Add specific components here as needed.</p>
          </div>
        );
    }
  };

  const tabs = [
    { icon: LayoutDashboard, label: 'Dashboard' },
    { icon: Truck, label: 'Live Shipments' },
    { icon: TrendingUp, label: 'AI Predictions' },
    { icon: Warehouse, label: 'Warehouses' },
    { icon: PackageCheck, label: 'Orders & Inventory' },
    { icon: BarChart3, label: 'Reports' },
    { icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="flex min-h-screen bg-[#f8f9fa]">
      {/* Sidebar */}
      <div className="w-[224px] bg-[#0f172a] text-white flex flex-col">
        <div className="p-6 border-b border-[#1e293b] mb-4">
          <h1 className="text-xl font-bold">AI Supply Chain</h1>
        </div>
        <div className="flex flex-col space-y-1 px-2">
          {tabs.map(({ icon: Icon, label }) => (
            <SidebarItem
              key={label}
              icon={<Icon size={20} />}
              label={label}
              active={activeTab === label}
              onClick={() => setActiveTab(label)}
            />
          ))}
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
        {renderContent()}
      </div>
    </div>
  );
};

interface SidebarItemProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

const SidebarItem: React.FC<SidebarItemProps> = ({ icon, label, active = false, onClick }) => (
  <div
    className={`flex items-center py-2 px-3 rounded-md cursor-pointer ${active ? 'bg-[#1e293b] font-medium' : 'hover:bg-[#1e293b] text-gray-300'}`}
    onClick={onClick}
  >
    <div className="mr-3">{icon}</div>
    <span>{label}</span>
  </div>
);

export default Dashboard;
