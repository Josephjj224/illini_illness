import React, {useEffect} from 'react';
import {ColorModeSwitcher} from './components/ColorModeSwitcher';
import {Route, Routes, useNavigate} from "react-router-dom";

import useAuth from "./hooks/useAuth";
import Home from "./pages/Home";
import Err404 from "./pages/Err404";
import Login from "./pages/Login";
import CheckIn from "./pages/CheckIn";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Symptom from "./pages/Symptom";
import History from "./pages/History";
import Transaction from "./pages/Transaction";
import "./styles/globals.scss";

const App = () => {
    return <>
        <ColorModeSwitcher pos="absolute" top=".8em" right=".8em" />
        <Routes>
            <Route index Component={Home} />
            <Route path="/home" Component={Home} />
            <Route path="/login" Component={Login} />
            <Route path="/register" Component={Register} />
            <Route path="/dashboard" Component={Symptom} />
            <Route path="/check-in" Component={CheckIn} />
            <Route path="/history" Component={History} />
            <Route path="/transaction" Component={Transaction} />
            <Route path="*" Component={Err404} />
        </Routes>
    </>
}

export default App;
