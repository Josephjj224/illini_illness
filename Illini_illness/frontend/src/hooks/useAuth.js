import { useState, useEffect } from "react";

const useAuth = () => {
    const getUserID = () => localStorage.getItem("userID")|| "yiyangx7";
    const getFirstName = () => localStorage.getItem("firstName")|| "Yiyang";
    const getLastName = () => localStorage.getItem("lastName")|| "Xu";;
    const getUserRole = () => localStorage.getItem("userRole")|| "doctor";;

    const [userID, setUserID] = useState(getUserID());
    const [userRole, setUserRole] = useState(getUserRole());
    const [firstName, setFirstName] = useState(getFirstName());
    const [lastName, setLastName] = useState(getLastName());

    const setUserData = ({ ID, role, firstName, lastName }) => {
        localStorage.setItem("userID", ID);
        localStorage.setItem("userRole", role);
        localStorage.setItem("firstName", firstName);
        localStorage.setItem("lastName", lastName);

        setUserID(ID);
        setUserRole(role);
        setFirstName(firstName);
        setLastName(lastName);
    };

    const clearUserData = () => {
        localStorage.clear();
        setUserID(null);
        setUserRole(null);
        setFirstName(null);
        setLastName(null);
    };

   
    useEffect(() => {
        setUserID(getUserID());
        setUserRole(getUserRole());
        setFirstName(getFirstName());
        setLastName(getLastName());
    }, []);

    return { userID, userRole, firstName, lastName, setUserData, clearUserData };
};

export default useAuth;
