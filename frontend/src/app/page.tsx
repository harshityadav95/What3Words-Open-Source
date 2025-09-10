'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import map component to avoid SSR issues
const MapComponent = dynamic(() => import('../components/MapComponent'), { ssr: false });

// Import CSS
import 'leaflet/dist/leaflet.css';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8081';

export default function Home() {
  const [lat, setLat] = useState('');
  const [lng, setLng] = useState('');
  const [word1, setWord1] = useState('');
  const [word2, setWord2] = useState('');
  const [word3, setWord3] = useState('');
  const [resultWords, setResultWords] = useState('');
  const [resultCoords, setResultCoords] = useState('');
  const [mapPosition, setMapPosition] = useState<[number, number]>([51.505, -0.09]);
  const [mapWords, setMapWords] = useState('');

  const convertCoordsToWords = async () => {
    const latNum = parseFloat(lat);
    const lngNum = parseFloat(lng);

    if (isNaN(latNum) || latNum < -90 || latNum > 90) {
      setResultWords('Error: Invalid latitude (-90 to 90)');
      return;
    }
    if (isNaN(lngNum) || lngNum < -180 || lngNum > 180) {
      setResultWords('Error: Invalid longitude (-180 to 180)');
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/convert-coords`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: latNum, longitude: lngNum }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultWords(`${data.word1} ${data.word2} ${data.word3}`);
      } else {
        setResultWords(`Error: ${data.detail}`);
      }
    } catch (error) {
      setResultWords('Error connecting to backend');
    }
  };

  const convertWordsToCoords = async () => {
    if (!word1.trim() || !word2.trim() || !word3.trim()) {
      setResultCoords('Error: All three words are required');
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/convert-words`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word1: word1.toLowerCase(), word2: word2.toLowerCase(), word3: word3.toLowerCase() }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultCoords(`${data.latitude}, ${data.longitude}`);
      } else {
        setResultCoords(`Error: ${data.detail}`);
      }
    } catch (error) {
      setResultCoords('Error connecting to backend');
    }
  };

  const handleMapClick = async (lat: number, lng: number) => {
    setMapPosition([lat, lng]);
    try {
      const response = await fetch(`${API_BASE}/convert-coords`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: lat, longitude: lng }),
      });
      const data = await response.json();
      if (response.ok) {
        setMapWords(`${data.word1} ${data.word2} ${data.word3}`);
      } else {
        setMapWords(`Error: ${data.detail}`);
      }
    } catch (error) {
      setMapWords('Error connecting to backend');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          What3Words Clone
        </h1>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Coordinates to Words */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">
              Coordinates to Words
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  Latitude
                </label>
                <input
                  type="number"
                  step="any"
                  value={lat}
                  onChange={(e) => setLat(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 51.5074"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  Longitude
                </label>
                <input
                  type="number"
                  step="any"
                  value={lng}
                  onChange={(e) => setLng(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., -0.1278"
                />
              </div>
              <button
                onClick={convertCoordsToWords}
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Convert to Words
              </button>
              {resultWords && (
                <div className="mt-4 p-3 bg-gray-50 rounded-md">
                  <p className="text-sm font-medium text-gray-600">Result:</p>
                  <p className="text-lg font-mono text-gray-800">{resultWords}</p>
                </div>
              )}
            </div>
          </div>

          {/* Words to Coordinates */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">
              Words to Coordinates
            </h2>
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">
                    Word 1
                  </label>
                  <input
                    type="text"
                    value={word1}
                    onChange={(e) => setWord1(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="first"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">
                    Word 2
                  </label>
                  <input
                    type="text"
                    value={word2}
                    onChange={(e) => setWord2(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="second"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-1">
                    Word 3
                  </label>
                  <input
                    type="text"
                    value={word3}
                    onChange={(e) => setWord3(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="third"
                  />
                </div>
              </div>
              <button
                onClick={convertWordsToCoords}
                className="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                Convert to Coordinates
              </button>
              {resultCoords && (
                <div className="mt-4 p-3 bg-gray-50 rounded-md">
                  <p className="text-sm font-medium text-gray-600">Result:</p>
                  <p className="text-lg font-mono text-gray-800">{resultCoords}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Interactive Map Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-gray-700">
            Interactive Map - Click to Get Words
          </h2>
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">
              Click anywhere on the map to get the three-word address for that location
            </p>
            {mapWords && (
              <div className="p-3 bg-blue-50 rounded-md">
                <p className="text-sm font-medium text-gray-600">Selected Location Words:</p>
                <p className="text-lg font-mono text-blue-800">{mapWords}</p>
                <p className="text-sm text-gray-500 mt-1">
                  Coordinates: {mapPosition[0].toFixed(6)}, {mapPosition[1].toFixed(6)}
                </p>
              </div>
            )}
          </div>
          <div className="h-96 w-full rounded-lg overflow-hidden border">
            <MapComponent
              onLocationSelect={handleMapClick}
              initialPosition={mapPosition}
              words={mapWords}
            />
          </div>
        </div>

        <div className="mt-8 text-center text-gray-600">
          <p>Open source What3Words clone built with FastAPI and Next.js</p>
        </div>
      </div>
    </div>
  );
}