import React from 'react';

interface StationStatsCardProps {
  stationName: string;
  recordCount?: number;
  temperaturePrediction?: number;
  predictionUnit?: string;
}

const StationStatsCard: React.FC<StationStatsCardProps> = ({
  stationName,
  recordCount,
  temperaturePrediction,
  predictionUnit,
}) => {
  return (
    <div className="bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 shadow-md rounded-lg p-6 flex flex-col items-center justify-center">
      <h2 className="text-2xl font-bold mb-4">Estatísticas da Estação</h2>
      <p className="text-lg mb-2">
        <span className="font-semibold">Estação:</span> {stationName}
      </p>
      {recordCount !== undefined && (
        <p className="text-lg mb-2">
          <span className="font-semibold">Total de Registros:</span> {recordCount}
        </p>
      )}
      {temperaturePrediction !== undefined && (
        <p className="text-lg mb-2">
          <span className="font-semibold">Previsão de Temperatura (Média):</span> {temperaturePrediction} {predictionUnit}
        </p>
      )}
      {recordCount === undefined && temperaturePrediction === undefined && (
        <p className="text-gray-500">Carregando estatísticas...</p>
      )}
    </div>
  );
};

export default StationStatsCard;
