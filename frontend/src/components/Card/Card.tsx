import styles from './Card.module.scss'

import { useContext } from 'react'

import { SelectSystemContext } from '../../utils/context/index.tsx'

function Card() {


    const { selectedSystem } = useContext(SelectSystemContext)

    return (
        <>
            <div className={styles.main}>
                <h1>{selectedSystem.site_public_name}</h1>
                {"Type : " + selectedSystem.type} <br />
                {"Total area : " + selectedSystem.area + "m²"} <br />
                {"Maximum power : " + selectedSystem.power + "kW"} < br />
                {"Site elevation : " + selectedSystem.site_elevation + "m"} < br />
                {"Climate type : " + selectedSystem.climate_type} < br />
                {"Average temperature : " + selectedSystem.av_temp} < br />
                {"Module manufacturer : " + selectedSystem.manufacturer} < br />
                {"Module model : " + selectedSystem.model} < br />
            </div>
        </>
    )
}

export { Card }