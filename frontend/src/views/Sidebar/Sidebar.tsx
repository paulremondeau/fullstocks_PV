import styles from './Sidebar.module.scss'

import { Link } from 'react-router-dom'


function Sidebar() {
    return (<>
        <div className={styles.main}>
            <h3>Filters</h3>
        </div>
    </>)
}

export { Sidebar }