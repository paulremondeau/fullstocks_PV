import styles from './System.module.scss'

import { Card } from '../Card/Card.tsx'
import { Chart } from '../Chart/Chart.tsx'

import { useContext } from 'react'

import { SystemContext } from '../../utils/context/index.tsx'

import Plot from 'react-plotly.js';

function System() {

    const dataChart = useContext(SystemContext);

    return (
        <>
            <div className={styles.main}>
                <Card />
                <div className={styles.plots}>
                    <Plot
                        data={dataChart.monthly_chart.data}
                        layout={dataChart.monthly_chart.layout}
                    />
                    <Plot
                        data={dataChart.daily_chart.data}
                        layout={dataChart.daily_chart.layout}
                    />
                </div>
            </div>
        </>
    )
}

export { System }