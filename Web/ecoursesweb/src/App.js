import logo from './logo.svg';
import React, { useReducer, createContext } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import Home from './component/Home';
import Buses from './component/Buses';
import Login from './component/Login';
import BusesDetail from './component/BusesDetail';
import myReducer from './reducers/UserReducer';
import Header from './layout/Header';
import 'bootstrap/dist/css/bootstrap.min.css';
import Footer from './layout/Footer';
import cookies from 'react-cookies'
import Register from './component/Register'

export const UserContext = createContext()

const App = () => {
  const [user, dispatch] = useReducer(myReducer, cookies.load('current_user'))

  return (
    <BrowserRouter>
      <UserContext.Provider value={[user, dispatch]}>
        <Header />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/route/:routeId/buses" element={<Buses />} />
          <Route path="/login" element={<Login />} />
          <Route path="/buses/:busesId" element={<BusesDetail />} />
          <Route path="/register" element={<Register />} />
        </Routes>

        <Footer />
      </UserContext.Provider>
    </BrowserRouter>
  )
}

export default App