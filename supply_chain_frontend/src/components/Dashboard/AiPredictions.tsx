import React, { useEffect, useState } from "react";

interface PerformanceData {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  // Add other fields depending on your backend response
}

interface ApiResponse {
  status: string;
  message: string;
  data: PerformanceData;
  errors: { field: string; message: string }[]; // Replace with the actual structure of the errors array
}

type Props = {
  modelId: string;
};

const ModelPerformance: React.FC<Props> = ({ modelId }) => {
  const [performance, setPerformance] = useState<PerformanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPerformance = async () => {
      try {
        const res = await fetch(
          `${import.meta.env.VITE_BASE_API_URL}/ai/models/${modelId}/performance`
        );
        if (!res.ok) {
          throw new Error("Failed to fetch performance");
        }

        const result: ApiResponse = await res.json();
        setPerformance(result.data);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPerformance();
  }, [modelId]);

  if (loading) return <p className="text-blue-500">Loading...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (!performance) return <p className="text-yellow-500">No data available</p>;

  return (
    <div className="p-4 bg-white rounded-2xl shadow-md max-w-md mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4 text-center">Model Performance</h2>
      <ul className="space-y-2">
        <li>Accuracy: <span className="font-medium">{performance.accuracy}</span></li>
        <li>Precision: <span className="font-medium">{performance.precision}</span></li>
        <li>Recall: <span className="font-medium">{performance.recall}</span></li>
        <li>F1 Score: <span className="font-medium">{performance.f1_score}</span></li>
        {/* Add more fields if necessary */}
      </ul>
    </div>
  );
};

export default ModelPerformance;
