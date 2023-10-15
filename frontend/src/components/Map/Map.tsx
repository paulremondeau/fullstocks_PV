import 'leaflet/dist/leaflet.css'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'

import { AvailableDataContext, SelectSystemContext } from '../../utils/context/index.tsx'

import { useContext } from 'react'

// Leaflet Markers
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;


function Map() {

    const availableData = useContext(AvailableDataContext)
    const { setSelectedSystem } = useContext(SelectSystemContext)

    return <>
        <MapContainer style={{ height: "100%", width: "100%" }} center={{ lat: 39.011902, lng: -98.4842465 }} zoom={5} scrollWheelZoom={true}>
            <TileLayer
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>  contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {Object.keys(availableData).map((key: string) => {
                const position = { lat: availableData[+key].site_latitude as number, lng: availableData[+key].site_longitude as number }
                return (

                    <Marker position={position} eventHandlers={{
                        click: () => {
                            setSelectedSystem(availableData[+key])
                        }
                    }}>
                        <Popup>

                            {availableData[+key].site_public_name} <br />
                            {"Type : " + availableData[+key].type} <br />
                            {"Total area : " + availableData[+key].area + "m²"} <br />
                            {"Maximum power : " + availableData[+key].power + "kW"} < br />
                            {"Site elevation : " + availableData[+key].site_elevation + "m"} < br />
                            {"Climate type : " + availableData[+key].climate_type} < br />
                            {"Average temperature : " + availableData[+key].av_temp} < br />
                            {"Module manufacturer : " + availableData[+key].manufacturer} < br />
                            {"Module model : " + availableData[+key].model} < br />
                        </Popup>
                    </Marker>

                )
            })}
        </MapContainer>
    </>
}

export { Map }