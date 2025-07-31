'use client';

import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import StationStatsCard from './components/StationStatsCard';
import WeatherCard from './components/WeatherCard';

interface SensorData {
  sensor_name: string;
  sensor_type: string;
  value: number;
  unit: string;
  timestamp: string;
}

interface Station {
  station_id: string;
  city: string;
  latitude: string;
  longitude: string;
}

interface RecordCountResponse {
  station_id: string;
  record_count: number;
}

interface TemperaturePredictionResponse {
  station_id: string;
  prediction: number | null;
  message?: string;
  unit?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';
const STATION_ID = 'STATION_FORTALEZA_001';

export default function Home() {
  // Query para buscar dados da estação
  const { data: station, isLoading: isLoadingStation, error: errorStation } = useQuery<Station>({
    queryKey: ['station', STATION_ID],
    queryFn: async () => {
      const response = await axios.get<Station>(`${API_BASE_URL}/stations/${STATION_ID}/`);
      return response.data;
    },
  });

  // Query para buscar os últimos dados de sensores, com refetch a cada 15 segundos
  const { data: sensorData, isLoading: isLoadingSensorData, error: errorSensorData } = useQuery<SensorData[]>({
    queryKey: ['sensorData', STATION_ID],
    queryFn: async () => {
      const response = await axios.get<SensorData[]>(`${API_BASE_URL}/sensor_data/latest/?station_id=${STATION_ID}`);
      return response.data;
    },
    refetchInterval: 3000, // Refetch a cada 15 segundos
    staleTime: 0, // Dados sempre considerados 'stale'
    enabled: true, 
  });

  // Query para buscar o número de registros
  const { data: recordCountData, isLoading: isLoadingRecordCount, error: errorRecordCount } = useQuery<RecordCountResponse>({
    queryKey: ['recordCount', STATION_ID],
    queryFn: async () => {
      const response = await axios.get<RecordCountResponse>(`${API_BASE_URL}/sensor_data/record_count/?station_id=${STATION_ID}`);
      return response.data;
    },
    refetchInterval: 3000, // Refetch a cada 60 segundos
    enabled: true, 
  });

  // Query para buscar a previsão de temperatura
  const { data: tempPredictionData, isLoading: isLoadingTempPrediction, error: errorTempPrediction } = useQuery<TemperaturePredictionResponse>({
    queryKey: ['tempPrediction', STATION_ID],
    queryFn: async () => {
      const response = await axios.get<TemperaturePredictionResponse>(`${API_BASE_URL}/sensor_data/temperature_prediction/?station_id=${STATION_ID}`);
      return response.data;
    },
    refetchInterval: 3000, // Refetch a cada 60 segundos
    enabled: true, 
  });

  const error = errorStation || errorSensorData || errorRecordCount || errorTempPrediction;
  const isLoading = isLoadingStation || isLoadingSensorData || isLoadingRecordCount || isLoadingTempPrediction;

  // Mapear os dados dos sensores para facilitar o acesso no WeatherCard
  const mappedSensorData: { [key: string]: SensorData } = {};
  if (sensorData) {
    sensorData.forEach(sensor => {
      if (sensor.sensor_type === 'temperature') mappedSensorData.temperature = sensor;
      if (sensor.sensor_type === 'humidity') mappedSensorData.humidity = sensor;
      if (sensor.sensor_type === 'rain') mappedSensorData.rain = sensor;
      if (sensor.sensor_type === 'wind_speed') mappedSensorData.windSpeed = sensor;
    });
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">Estação Meteorológica</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          <strong className="font-bold">Erro!</strong>
          <span className="block sm:inline"> {error.message}</span>
        </div>
      )}

      {isLoading ? (
        <p className="text-center text-gray-500">Carregando dados...</p>
      ) : station ? (
        <div className="flex flex-wrap justify-center gap-6 mb-6">
          <WeatherCard
            stationName={station.city}
            temperature={mappedSensorData.temperature}
            humidity={mappedSensorData.humidity}
            rain={mappedSensorData.rain}
            windSpeed={mappedSensorData.windSpeed}
          />
          <StationStatsCard
            stationName={station.city}
            recordCount={recordCountData?.record_count}
            temperaturePrediction={tempPredictionData?.prediction || undefined}
            predictionUnit={tempPredictionData?.unit || undefined}
          />
        </div>
      ) : (
        <p className="text-center text-gray-500">Nenhum dado da estação disponível.</p>
      )}
    </div>
  );
}
