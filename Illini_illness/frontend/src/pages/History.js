import {
    Button, ButtonGroup,
    Center,
    Heading,
    Progress,
    Spinner,
    Tab,
    TabList,
    useToast,
    TabPanel,
    TabPanels,
    Tabs,
    Text
} from "@chakra-ui/react";
import axios from "axios";
import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import Main from "../components/Main";
import useAuth from "../hooks/useAuth";
import "../styles/history.scss";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const History = () => {
    const [conditions, setConditions] = useState(false);
    const [symptoms, setSymptoms] = useState(false);
    // const [treatments, setTreatments] = useState(false);
    const [param, setParam] = useState('');  // 用于存储参数的 state
    const [viewingConditions, setViewingConditions] = useState(true);
    const nav = useNavigate();
    const {userID} = useAuth();

    useEffect(() => {
        document.title = "Medical History";

        if (!userID) {
            nav("/login");
        }

        if (!conditions) {
            axios.get("http://34.41.122.202:5000/api/condition", {
                params: {
                    patID: userID,
                    fetch_all: true
                }
            }).then(res => {
                console.log(res.data);
                setConditions(res.data.data);
            }).catch(err => console.log(err));
        }
        if (!symptoms) {
            axios.get("http://34.41.122.202:5000/api/symptom", {
                params: {
                    patID: userID,
                    fetch_all: true
                }
            }).then(res => {
                console.log(res.data);
                setSymptoms(res.data.data);
            }).catch(err => console.log(err));
        }
        // if (!treatments) {
        //     axios.get("http://127.0.0.1:5000/api/treatment", {
        //         params: {
        //             patID: "QEVuQwEA66EJ4oOf7mD5xYzgc9nrSw=="
        //         }
        //     }).then(res => {
        //         console.log(res.data);
        //         setTreatments(res.data.data);
        //     }).catch(err => console.log(err));
        // }
    }, [userID]);

    const executeProcedure = async () => {
        try {
            toast('Your Status Check Request Haas been sent to your Doctor', {
                position: 'top-right',
                autoClose: 5000, // 5 seconds
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
            });
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
        <Tabs
            width="100%"
            height="100%"
            colorScheme={viewingConditions ? "red" : "blue"}
            onChange={() => setViewingConditions(!viewingConditions)}
        >
            <TabList>
                <Tab>Conditions</Tab>
                <Tab>Symptoms</Tab>
            </TabList>
            <ToastContainer />
            <ButtonGroup>
                <Button onClick={executeProcedure}>Check Alert</Button>
            </ButtonGroup>

            <TabPanels height="100%">
                <TabPanel height="100%" padding="1em 0">
                    {conditions ? conditions.map(({checkDate, rate, condDesc}, i) => (
                        <Progress className="progress" colorScheme="red" value={rate * 20} key={i}>
                            <Text color="blackAlpha" className="progress-text">{condDesc}</Text>
                            <Text color="blackAlpha" className="progress-text" as="i">{checkDate}</Text>
                        </Progress>
                    )) : <Center height="100%"><Spinner color="red.600" thickness="2px" size="lg" /></Center>}
                </TabPanel>
                <TabPanel height="100%" padding="1em 0">
                    {symptoms ? symptoms.map(({checkDate, rate, sympDesc}, i) => (
                        <Progress className="progress" colorScheme="blue" value={rate * 20} key={i}>
                            <Text color="blackAlpha" className="progress-text">{sympDesc}</Text>
                            <Text color="blackAlpha" className="progress-text" as="i">{checkDate}</Text>
                        </Progress>
                    )) : <Center height="100%"><Spinner color="red.600" thickness="2px" size="lg" /></Center>}
                </TabPanel>
            </TabPanels>
        </Tabs>
    </Main>;
};

export default History;
