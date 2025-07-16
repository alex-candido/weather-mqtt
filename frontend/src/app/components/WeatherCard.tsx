import React, { useEffect, useState } from 'react';

interface SensorData {
  sensor_name: string;
  sensor_type: string;
  value: number;
  unit: string;
  timestamp: string;
}

interface WeatherCardProps {
  stationName: string;
  temperature?: SensorData;
  humidity?: SensorData;
  rain?: SensorData;
  windSpeed?: SensorData;
}

const WeatherCard: React.FC<WeatherCardProps> = ({
  stationName,
  temperature,
  humidity,
  rain,
  windSpeed,
}) => {
  const [animate, setAnimate] = useState(false);

  // Lógica para determinar o ícone e as classes de estilo
  let icon = '☀️'; // Ensolarado por padrão
  let bgColorClass = 'bg-yellow-200 dark:bg-yellow-700';
  let textColorClass = 'text-yellow-800 dark:text-yellow-100';

  if (rain && rain.value > 0) {
    icon = '🌧️'; // Chuva
    bgColorClass = 'bg-blue-200 dark:bg-blue-700';
    textColorClass = 'text-blue-800 dark:text-blue-100';
  } else if (humidity && humidity.value > 70) {
    icon = '☁️'; // Nublado
    bgColorClass = 'bg-gray-200 dark:bg-gray-700';
    textColorClass = 'text-gray-800 dark:text-gray-100';
  } else if (temperature && temperature.value < 15) {
    icon = '🥶'; // Frio
    bgColorClass = 'bg-blue-100 dark:bg-blue-800';
    textColorClass = 'text-blue-700 dark:text-blue-200';
  } else if (temperature && temperature.value > 30) {
    icon = '🥵'; // Quente
    bgColorClass = 'bg-red-200 dark:bg-red-700';
    textColorClass = 'text-red-800 dark:text-red-100';
  }

  // Dispara a animação quando a temperatura muda
  useEffect(() => {
    console.log(temperature)
    if (temperature?.value !== undefined) {
      console.log('Temperatura mudou, disparando animação!', temperature.value);
      setAnimate(true);
      const timer = setTimeout(() => {
        setAnimate(false);
        console.log('Animação finalizada.');
      }, 500); // Duração da animação
      return () => clearTimeout(timer);
    }
  }, [temperature?.timestamp]);

  return (
    <div
      className={`flex flex-col items-center justify-center p-6 rounded-lg shadow-lg ${bgColorClass} ${textColorClass}`}
    >
      <div className={`text-6xl mb-4 ${animate ? 'animate-pulse-once' : ''}`}>{icon}</div>
      <h2 className="text-2xl font-bold mb-2">{stationName}</h2>
      {temperature && (
        <p className="text-5xl font-semibold mb-2">
          {temperature.value}°{temperature.unit}
        </p>
      )}
      <div className="grid grid-cols-2 gap-2 text-lg">
        {humidity && (
          <p>
            Umidade: {humidity.value}{humidity.unit}
          </p>
        )}
        {windSpeed && (
          <p>
            Vento: {windSpeed.value}{windSpeed.unit}
          </p>
        )}
        {rain && (
          <p>
            Chuva: {rain.value}{rain.unit}
          </p>
        )}
      </div>
      <p className="text-sm mt-4">
        Última atualização: {temperature?.timestamp ? new Date(temperature.timestamp).toLocaleTimeString() : 'N/A'}
      </p>
    </div>
  );
};

export default WeatherCard;