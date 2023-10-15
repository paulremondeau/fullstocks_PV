import './App.scss';
import { Home } from './views/Home/Home'
import { Header } from './views/Header/Header'
import { Sidebar } from './views/Sidebar/Sidebar'

import { useState } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';

import { SelectSystemContext } from './utils/context/index'

function App() {

  const [selectedSystem, setSelectedSystem] = useState({})

  return (
    <>
      <Router>
        <SelectSystemContext.Provider value={{ selectedSystem, setSelectedSystem }}>
          <div className="app">

            <div className="header">
              <Header />
            </div>
            <div className="main">

              <div className="sidebar">
                <Sidebar />
              </div>

              <div className="home">
                <Home />
              </div>

            </div>
          </div>
        </SelectSystemContext.Provider>
      </Router>
    </>
  )
}

export default App
