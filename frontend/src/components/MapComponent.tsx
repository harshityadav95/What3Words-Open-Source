'use client';

import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import { useState } from 'react';
import L from 'leaflet';

// Fix Leaflet default icon paths to avoid 404 for marker icons in Next.js
// See: https://github.com/Leaflet/Leaflet/issues/4968
// @ts-ignore
delete (L.Icon.Default as any).prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});


interface MapComponentProps {
  onLocationSelect: (lat: number, lng: number) => void;
  initialPosition: [number, number];
  words: string;
}

function LocationMarker({ onLocationSelect, words }: { onLocationSelect: (lat: number, lng: number) => void; words: string }) {
  const [position, setPosition] = useState<[number, number] | null>(null);

  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      setPosition([lat, lng]);
      onLocationSelect(lat, lng);
    },
  });

  return position === null ? null : (
    <Marker position={position}>
      <Popup>{words || 'Click on map to get words'}</Popup>
    </Marker>
  );
}

export default function MapComponent({ onLocationSelect, initialPosition, words }: MapComponentProps) {
  return (
    <MapContainer
      center={initialPosition}
      zoom={13}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <LocationMarker onLocationSelect={onLocationSelect} words={words} />
    </MapContainer>
  );
}