import {
    Button,
    ButtonGroup,
    Input,
    Center,
    Heading,
    Progress,
    Spinner,
    Tab,
    TabList,
    TabPanel,
    TabPanels,
    Tabs,
    Text
} from "@chakra-ui/react";
import axios from "axios";
import React, {useEffect, useState} from "react";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {useNavigate} from "react-router-dom";
import Main from "../components/Main";
import useAuth from "../hooks/useAuth";
import "../styles/history.scss";

const Transaction = () => {
    const [conditions, setConditions] = useState(false);
    const [symptoms, setSymptoms] = useState(false);
    // const [treatments, setTreatments] = useState(false);
    const [param, setParam] = useState('');  // 用于存储参数的 state
    const [viewingConditions, setViewingConditions] = useState(true);
    const nav = useNavigate();
    const {userID} = useAuth();

        const executeProcedure = async () => {
            try {
                const response = await fetch('http://34.41.122.202:5000/api/execute-procedure', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({patID: userID})  // 发送参数
                });
                const data = await response.json();
                console.log(data);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        return <Main justifyContent="flex-start" py="4em">
            <ButtonGroup>
                <Button onClick={executeProcedure}>Check Alert</Button>
            </ButtonGroup>
        </Main>;
    }

    export default Transaction;
