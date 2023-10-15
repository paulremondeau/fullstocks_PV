import styles from './Home.module.scss'

import { Map } from '../../components/Map/Map'
import { System } from '../../components/System/System'

import { Route, Routes } from 'react-router-dom'

import { useEffect, useState } from 'react'

import axios from 'axios';
import BACKEND_URL from '../../../config';

import { SystemInterface, AvailableData, SystemContext, AvailableDataContext } from '../../utils/context/index'

function Home() {

    const [availableSystems, setAvailableSystems] = useState<AvailableData>({})
    const [systemData, setSystemData] = useState<SystemInterface>({
        "info": [],
        "monthly_chart": { "data": [], "layout": {} },
        "daily_chart": { "data": [], "layout": {} },
    })

    useEffect(() => {
        axios
            .get(BACKEND_URL + "/send_graph")
            .then((res) => {
                setSystemData(() => {
                    return ({
                        "info": res.data.info,
                        "monthly_chart": JSON.parse(res.data.monthly_chart),
                        "daily_chart": JSON.parse(res.data.daily_chart)
                    })
                })
            }).catch((err) => {
                console.log(err)
            })

        axios
            .get(BACKEND_URL + "system_metadata")
            .then((res) => {

                const data: { [key: number]: string } = res.data
                setAvailableSystems(() => {
                    var newVal: { [key: string]: { [key: string]: number | string } } = {}

                    for (const [key, value] of Object.entries(data)) {
                        newVal[key] = JSON.parse(value)
                    }
                    return newVal
                })

            })
    }, [])


    return <>
        <div className={styles.main}>
            <Routes>
                <Route path="/" element={
                    <div className={styles.map}>
                        <AvailableDataContext.Provider value={availableSystems}>

                            <Map />

                        </AvailableDataContext.Provider>
                    </div>
                } />
                <Route path="/system" element={
                    <SystemContext.Provider value={systemData}>
                        <System />
                    </SystemContext.Provider>
                } />
            </Routes>

        </div>
    </>
}

export { Home }