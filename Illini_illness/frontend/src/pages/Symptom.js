import React, {useEffect, useState} from "react";
import {
    Heading,
    Stack,
    theme,
    Flex,
    Button,
    ButtonGroup,
    Box,
    Input,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalCloseButton,
    ModalBody,
    Text
} from "@chakra-ui/react";
import axios from 'axios';
import {Link, useNavigate} from "react-router-dom";
import Main from "../components/Main";
import useAuth from "../hooks/useAuth";
import InputSlider from "../components/InputSlider";

const CheckIn = () => {
    const {userID, firstName, lastName, clearUserData} = useAuth();
    const [symptomRate, setSymptomRate] = useState(0); // State for the symptom rate
    const [selectedType, setSelectedType] = useState('check-in'); // symptom condition or treatment
    const [symptoms, setSymptoms] = useState([]); // list to display
    const [selectedSymptom, setSelectedSymptom] = useState({
        desc: "",
        rate: 0,
        checkDate: null,
        patID: userID
    });
    const nav = useNavigate();
    const [greeting, setGreeting] = useState('');
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        document.title = "Check In";

        if (!userID) {
            nav("/login");
        }
    }, [userID, nav]);

    useEffect(() => {
        console.log("User info from useAuth:", {firstName, lastName});
    }, [firstName, lastName]);

    useEffect(() => {
        const greetings = [
            "Hello 👋", "🇪🇸 Hola 👋", "🇫🇷 Bonjour 👋", "🇩🇪 Hallo 👋", "🇮🇹 Ciao 👋", "🇷🇺 Привет 👋",
            "🇯🇵 こんにちは 👋", "🇰🇷 안녕하세요 👋", "🇨🇳 你好 👋", "🇮🇳 नमस्ते 👋", "🇹🇷 Merhaba 👋", "🇸🇪 Hej 👋", "🇳🇴 Hei 👋", "🇿🇦 Sawubona 👋", "Howdy🤠"
        ];
        setGreeting(greetings[Math.floor(Math.random() * greetings.length)]);
    }, []);

    useEffect(() => {
        console.log(selectedType);
        if (selectedType && selectedType !== "check-in") {
            axios.get('http://34.41.122.202:5000/api/' + selectedType, {
                params: {
                    patID: userID,
                    fetch_all: true
                }
            }).then(res => {
                console.log(res.data);
                setSymptoms(res.data.data);
            }).catch(err => console.log(err));
        }
        else if (selectedType === "check-in") {
            let items = [];

            axios.post('http://34.41.122.202:5000/api/condition', {
                patID: userID,
                action: "findPat",
                checkDate: today()
            }).then(res => {
                console.log(res.data);
                items = res.data.data || [];

                axios.post('http://34.41.122.202:5000/api/symptom', {
                    patID: userID,
                    action: "findPat",
                    checkDate: today()
                }).then(res => {
                    console.log(res.data);
                    let tmp = res.data.data || [];
                    items = [...items, ...tmp];

                    axios.post('http://34.41.122.202:5000/api/treatment', {
                        patID: userID,
                        action: "findPat",
                        checkDate: today()
                    }).then(res => {
                        console.log(res.data);
                        let tmp = res.data.data || [];
                        setSymptoms([...items, ...tmp]);
                    }).catch(err => console.log(err));
                }).catch(err => console.log(err));
            }).catch(err => console.log(err));
        }
    }, [selectedType]);

    const today = () => {
        const d = new Date()
        return new Date(d.getTime() - d.getTimezoneOffset() * 60 * 1000).toISOString().split('T')[0]
    }

    const rateDescription = (value) => {
        return value === 0 ? "not noticeable"
            : value === 1 ? "slightly active"
                : value === 2 ? "moderate"
                    : value === 3 ? "active"
                        : "very active";
    };


    const handleSearch = async () => {

        if (!searchTerm) {
            console.log("no search term");
            return;
        }

        try {
            const searchData = {
                patID: userID,
                action: "findPat",
                page_size: 10000
            };
            searchData[selectedType === "symptom" ? "sympDesc"
                : selectedType === "condition" ? "condDesc"
                : "treatDesc"] = searchTerm;
            console.log(searchData);

            const response = await axios.post('http://34.41.122.202:5000/api/' + selectedType, searchData);

            console.log(response.data);

            const searchResultsData = response.data.data;

            if (!searchResultsData) {
                setSymptoms([]);
            } else {
                setSymptoms(searchResultsData); // Update the symptoms state with search results
            }
        } catch (error) {
            console.error("An error occurred during the search:", error);
        }
    };

    const closeSymptomPopup = () => {
        setSelectedSymptom({...selectedSymptom, checkDate: null});
    };

    const addNewSymptom = () => {
        console.log(selectedType);
        console.log(selectedSymptom);
        // setSymptoms([selectedSymptom, ...symptoms]); // Add the new symptom to the state

        let {sympDesc, ...symp} = selectedSymptom;
        symp[selectedType === "symptom" ? "sympDesc"
            : selectedType === "condition" ? "condDesc"
            : "treatDesc"] = sympDesc || selectedSymptom.condDesc || selectedSymptom.treatDesc;
        console.log(symp);

        axios.post('http://34.41.122.202:5000/api/' + selectedType, {
            ...symp,
            patID: userID
        }).then(res => {
            console.log(res);

            axios.get('http://34.41.122.202:5000/api/' + selectedType, {
                params: {
                    patID: userID,
                    fetch_all: true
                }
            }).then(res => {
                console.log(res.data);
                setSymptoms(res.data.data);
            }).catch(err => console.log(err));
        }).catch(err => console.log(err));

        closeSymptomPopup();
    };

    const logout = () => {
        clearUserData();
    }

    const updateRate = (symp, i) => {
        console.log(symp);
        setSymptoms([...symptoms.slice(0, i), symp, ...symptoms.slice(i + 1)])
        axios.post('http://34.41.122.202:5000/api/symptom', {
            ...symp,
            patID: userID,
            action: "update"
        }).then(res => {
            console.log(res);
        }).catch(err => console.log(err));
    }

    const deleteSymp = (i) => {
        console.log(selectedSymptom);
        setSymptoms([...symptoms.slice(0, i), ...symptoms.slice(i + 1)])
        axios.post('http://34.41.122.202:5000/api/symptom', {
            sympID: selectedSymptom.sympID,
            action: "delete"
        }).then(res => {
            axios.get('http://34.41.122.202:5000/api/' + selectedType, {
                params: {
                    patID: userID,
                    fetch_all: true
                }
            }).then(res => {
                console.log(res.data);
                setSymptoms(res.data.data);
            }).catch(err => console.log(err));

            console.log(res);
        }).catch(err => console.log(err));

        closeSymptomPopup();
    }



    const capitalize = (str) => {
        return str.at(0).toUpperCase() + str.slice(1);
    }

    return (
        <Main margin="0" alignItems="center" maxWidth="none" justifyContent="flex-start" pt="10%">
            <Heading textAlign="center" as="h1" size="3xl" mb="4"> {greeting}</Heading>
            <Heading textAlign="center" as="h1" size="3xl" mb="4">
                Welcome Back, {firstName}! </Heading>
                <ButtonGroup variant="outline" spacing="6" my="4" flexWrap="wrap">
                    <Button onClick={() => setSelectedType("check-in")}>Daily Check-In</Button>
                    <Button onClick={() => setSelectedType("symptom")}>Symptom</Button>
                    <Button onClick={() => setSelectedType("condition")}>Condition</Button>
                    <Button onClick={() => setSelectedType("treatment")}>Treatment</Button>
                    <Button as={Link} to="/history">View History</Button>
                    <Button as={Link} to="/transaction">Alert</Button>
                    <Button onClick={logout}>Log Out</Button>
                </ButtonGroup>

            {selectedType === "check-in" ? symptoms.length === 0 ? "No Results"
                : symptoms.map((symptom, index) =>
                <InputSlider
                    title={symptom.sympDesc || symptom.condDesc || symptom.treatDesc || "No description"}
                    value={symptom.rate}
                    onChange={(value) => updateRate({...symptom, rate: value}, index)}
                    color={theme.colors.red}
                    key={index}
                    maxWidth="60%"
                />
            ) : <>
                <Box my="4">
                    <Flex align="center">
                        <Input
                            placeholder="Enter search term..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                        <ButtonGroup variant="outline" spacing="6" ml="2">
                            <Button onClick={handleSearch}
                                    disabled={!searchTerm}>Search</Button>
                            <Button onClick={() => setSelectedSymptom({
                                sympDesc: "",
                                rate: 0,
                                checkDate: today(),
                                action: "add"
                            })}>Add {capitalize(selectedType)}</Button>
                        </ButtonGroup>
                    </Flex>
                </Box>

                {symptoms.length === 0 && "No Results"}

                {symptoms.map((result, index) => (
                    <Flex key={index} align="center" mb="2">
                        <Box flex="1" mr="2">
                            <Input value={result.sympDesc || result.condDesc || result.treatDesc || 'No description'} isReadOnly />
                        </Box>
                        <Box flex="1" mr="2">
                            <Input value={rateDescription(result.rate)} isReadOnly />
                        </Box>
                        <Box flex="1" mr="2">
                            <Input value={result.checkDate || 'No date'} isReadOnly />
                        </Box>
                        <Button
                            colorScheme="red"
                            onClick={() => setSelectedSymptom({...result, action: "update"})}
                        >
                            Edit
                        </Button>
                    </Flex>
                ))}

                <Modal isOpen={selectedSymptom.checkDate} onClose={closeSymptomPopup}>
                    <ModalOverlay />
                    <ModalContent>
                        <ModalCloseButton />
                        {selectedSymptom.action === "update" ? (<>
                            <ModalHeader>Edit {capitalize(selectedType)}</ModalHeader>
                            <ModalBody padding="6" mt="-6">
                                <Box>Selected {capitalize(selectedType)}: {
                                    selectedSymptom.sympDesc || selectedSymptom.condDesc || selectedSymptom.treatDesc || "No description"
                                }</Box>
                                <Box>Current Rate: {rateDescription(selectedSymptom.rate)}</Box>

                                <InputSlider
                                    title="Update severity"
                                    color={theme.colors.red}
                                    value={selectedSymptom.rate}
                                    setValue={v => setSelectedSymptom({...selectedSymptom, rate: v})}
                                />
                                <Input
                                    type="date"
                                    mb="4"
                                    value={selectedSymptom.checkDate}
                                    onChange={(e) => setSelectedSymptom({...selectedSymptom, checkDate: e.target.value})}
                                />

                                <ButtonGroup>
                                    <Button colorScheme="red" onClick={addNewSymptom}>Update</Button>
                                    <Button colorScheme="red" onClick={deleteSymp} >Delete</Button>
                                </ButtonGroup>

                            </ModalBody>
                        </>) : (<>
                            <ModalHeader>Add a new {capitalize(selectedType)}</ModalHeader>
                            <ModalBody padding="6" mt="-6">
                                <Input
                                    placeholder="Enter description"
                                    mb="4"
                                    value={selectedSymptom.sympDesc}
                                    onChange={(e) => setSelectedSymptom({
                                        ...selectedSymptom,
                                        sympDesc: e.target.value
                                    })}
                                />
                                <InputSlider
                                    title="Update severity"
                                    color="red"
                                    value={selectedSymptom.rate}
                                    setValue={v => setSelectedSymptom({...selectedSymptom, rate: v})}
                                />
                                <Input
                                    type="date"
                                    mb="4"
                                    value={selectedSymptom.checkDate}
                                    onChange={(e) => setSelectedSymptom({...selectedSymptom, checkDate: e.target.value})}
                                />
                                <Flex dir="row" justifyContent="space-between">
                                    <Button onClick={closeSymptomPopup}>Close</Button>
                                    <Button colorScheme="red" onClick={addNewSymptom}>Add {capitalize(selectedType)}</Button>
                                </Flex>
                            </ModalBody>
                        </>)}
                    </ModalContent>
                </Modal>
            </>}
        </Main>
    );
};

export default CheckIn;

