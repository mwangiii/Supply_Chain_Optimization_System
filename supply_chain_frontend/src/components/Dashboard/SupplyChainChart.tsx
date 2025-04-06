import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';

// Sample data for the chart
const data = [
  { month: 'Jan', forecast: 3.8, actual: 2.8, warehouse: 1.4 },
  { month: 'Feb', forecast: 4.3, actual: 3.6, warehouse: 1.8 },
  { month: 'Mar', forecast: 6.0, actual: 4.2, warehouse: 2.3 },
  { month: 'Apr', forecast: 5.2, actual: 4.8, warehouse: 2.1 },
  { month: 'May', forecast: 7.0, actual: 5.5, warehouse: 2.8 },
  { month: 'Jun', forecast: 6.2, actual: 5.0, warehouse: 3.0 },
  { month: 'Jul', forecast: 4.5, actual: 6.8, warehouse: 3.3 },
  { month: 'Aug', forecast: 7.3, actual: 8.0, warehouse: 4.5 },
  { month: 'Sep', forecast: 6.0, actual: 7.5, warehouse: 4.2 },
  { month: 'Oct', forecast: 7.0, actual: 7.8, warehouse: 4.8 },
  { month: 'Nov', forecast: 8.5, actual: 6.5, warehouse: 5.0 },
  { month: 'Dec', forecast: 9.2, actual: 6.8, warehouse: 4.5 },
];

const SupplyChainChart: React.FC = () => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 30 }}
      >
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#eee" />
        <XAxis dataKey="month" tickLine={false} axisLine={false} />
        <YAxis tickLine={false} axisLine={false} domain={[0, 10]} tickCount={6} />
        <Tooltip />
        <Legend 
          align="left" 
          verticalAlign="bottom" 
          iconType="plainline" 
          wrapperStyle={{ paddingTop: '20px' }}
        />
        <Line 
          type="monotone" 
          dataKey="forecast" 
          stroke="#3b82f6" 
          strokeWidth={2} 
          dot={false} 
          activeDot={{ r: 4 }} 
          name="Forecast"
        />
        <Line 
          type="monotone" 
          dataKey="actual" 
          stroke="#0f172a" 
          strokeWidth={2} 
          dot={false} 
          activeDot={{ r: 4 }} 
          name="Actual"
        />
        <Line 
          type="monotone" 
          dataKey="warehouse" 
          stroke="#10b981" 
          strokeWidth={2} 
          strokeDasharray="5 5" 
          dot={false} 
          activeDot={{ r: 4 }} 
          name="Warehouse Performance"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default SupplyChainChart;
