import {useEffect} from "react";
import axios from "axios";
import {Link, useNavigate} from "react-router-dom";

import Button from "../components/Button";
import Main from "../components/Main";
import useAuth from "../hooks/useAuth";

const Dashboard = () => {
    const nav = useNavigate();
    const {userID, clearUserData} = useAuth();

    useEffect(() => {
        document.title = "Checkin"

        if (userID) {
            nav("/dashboard");
        }
    }, [userID]);
    

    const logout = () => {
        clearUserData();
    }

    return <Main>
        <Button as={Link} to="/Symptom" colorScheme="red" width="12em" mt="2">Daily Check-In</Button>
        <Button as={Link} to="/history" colorScheme="red" width="12em" mt="2">View History</Button>

        <Button onClick={logout} colorScheme="red" width="12em" mt="2">Log Out</Button>
    </Main>;
};

export default Dashboard;
