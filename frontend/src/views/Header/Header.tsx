import styles from './Header.module.scss';
import { Link } from 'react-router-dom'

import GitHub from '../../assets/github.svg'

import { SelectSystemContext } from '../../utils/context/index.tsx'

import { useContext } from 'react'

function Header() {

    const { selectedSystem } = useContext(SelectSystemContext)



    return (<>
        <div className={styles.main}>
            <h3 className={styles.title}>
                PV analysis
            </h3>
            <div className={styles.nav}>
                <Link to="/">
                    <button>Map</button>
                </Link>
                <Link to="/system">
                    <button>
                        System
                    </button>
                </Link>
                {"Selected system : " + selectedSystem.system_public_name}
            </div>
            <a href="https://paulremondeau.github.io">
                <img src={GitHub} className={styles.logo} />
            </a>
        </div>
    </>)
}

export { Header }