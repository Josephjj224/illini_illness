import React, { useEffect, useState } from "react";
import {
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
import { useNavigate } from "react-router-dom";
import Main from "../components/Main";
import useAuth from "../hooks/useAuth";

const CheckIn = () => {
    const [selectedType, setSelectedType] = useState('');
    const [symptoms, setSymptoms] = useState([]); // This will hold the user's symptoms
    const [newSymptom, setNewSymptom] = useState("");
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedSymptom, setSelectedSymptom] = useState(null);
    const nav = useNavigate();
    const { userID } = useAuth();
    const [searchCriteria, setSearchCriteria] = useState({
        // checkDate: "",
        sympDesc: "",
        action: "findPat", // Assuming you are searching by patient
        patID: userID
    });
    const [searchResults, setSearchResults] = useState([]);

    

    const rateDescription = (value) => {
        return value === 0 ? "not noticeable"
            : value === 1 ? "slightly active"
                : value === 2 ? "moderate"
                    : value === 3 ? "active"
                        : "very active";
    };

    useEffect(() => {
        console.log('hi');
        console.log(selectedType);
        axios.post('http://34.41.122.202:5000/api/' + selectedType, {
            patID: userID,
            // action: "findPat",
            // checkDate: new Date().toISOString().split('T')[0]
        }).then(res => {
            console.log(res.data);
            setSymptoms(res.data.data);
        }).catch(err => console.log(err));
    }, [selectedType]);

    const addSymptomToList = () => {
        axios.post("http://34.41.122.202:5000/api/symptom", {
            params: {
                patID: userID,
                sympDesc: newSymptom,
                rate: 0
            }
        }).then(res => console.log(res)).catch(err => console.log(err));

        if (newSymptom.trim() !== "") {
            setSymptoms([
                ...symptoms,
                {
                    id: symptoms.length, // You might want to use a better id generation strategy
                    sympDesc: newSymptom, // Assuming you want to add a new symptom description
                    rate: 0, // Assuming a default rate of 0 for new symptoms
                },
            ]);
            setNewSymptom("");
        }
    };

    const handleSearch = async () => {
        try {
            const response = await axios.post('http://34.41.122.202:5000/api/symptom', {
                ...searchCriteria,
                patID: userID, // Assume that userID is the patient ID you're searching for
            });

            setSearchResults(response.data.data); // Update the symptoms state with search results
        } catch (error) {
            console.error("An error occurred during the search:", error);
        }
    };

    const openSymptomPopup = (symptom) => {
        setSelectedSymptom(symptom);
        setIsModalOpen(true);
    };

    const closeSymptomPopup = () => {
        setSelectedSymptom(null);
        setIsModalOpen(false);
    };

    return (
        <Main>
            <Flex direction="column" align="center">
                <ButtonGroup variant="outline" spacing="6" my="4">
                    <Button onClick={() => setSelectedType("symptom")}>Symptom</Button>
                    <Button onClick={() => setSelectedType("condition")}>Condition</Button>
                    <Button onClick={() => setSelectedType("treatment")}>Treatment</Button>
                </ButtonGroup>
                {/* Search Section */}
                <Input
                    placeholder="Enter sympDesc..."
                    value={searchCriteria.sympDesc}
                    onChange={(e) => setSearchCriteria({ ...searchCriteria, sympDesc: e.target.value })}
                />
                <Button onClick={handleSearch} ml="2" disabled={!searchCriteria.sympDesc.trim()}>
                    Search
                </Button>

                {/* Display search results */}
                {searchResults.map((result, index) => (
                    <Flex key={index} align="center" mb="2">
                        <Box flex="1" mr="2">
                            <Input value={result.sympDesc || 'No description'} isReadOnly />
                        </Box>
                        <Box flex="1" mr="2">
                            <Input value={rateDescription(result.rate)} isReadOnly />
                        </Box>
                        <Box flex="1" mr="2">
                            <Input value={result.checkDate || 'No date'} isReadOnly />
                        </Box>
                        <Button
                            colorScheme="red"
                            onClick={() => openSymptomPopup(result)}
                        >
                            Edit
                        </Button>
                    </Flex>
                ))}
                {selectedType === "symptom" && (
                    <Box my="4">
                        <Input
                            placeholder="Add new symptom..."
                            value={newSymptom}
                            onChange={(e) => setNewSymptom(e.target.value)}
                        />
                        <Button onClick={addSymptomToList} ml="2">
                            Add Symptom
                        </Button>
                    </Box>
                )}

                {selectedType === "symptom" && symptoms.map((symptom, index) => (
                    <Flex key={index} align="center" mb="2">
                        <Box flex="1" mr="2">
                            <Input value={symptom.sympDesc || 'No description'} isReadOnly />
                        </Box>
                        <Box flex="1" mr="2">
                            <Input value={rateDescription(symptom.rate)} isReadOnly />
                        </Box>
                        <Box flex="1" mr="2">
                            <Input value={symptom.checkDate || 'No date'} isReadOnly />
                        </Box>
                        <Button
                            colorScheme="red"
                            onClick={() => openSymptomPopup(symptom)}
                        >
                            Edit
                        </Button>
                    </Flex>
                ))}

                <Modal isOpen={isModalOpen} onClose={closeSymptomPopup}>
                    <ModalOverlay />
                    <ModalContent>
                        <ModalHeader>Edit Symptom</ModalHeader>
                        <ModalCloseButton />
                        <ModalBody>
                            {selectedSymptom && (
                                <>
                                    <Box>Selected Symptom: {selectedSymptom.sympDesc || 'No description'}</Box>
                                    <Box>Rate: {rateDescription(selectedSymptom.rate)}</Box>
                                    {/* Add additional form elements or inputs for editing symptom here */}
                                </>
                            )}
                        </ModalBody>
                    </ModalContent>
                </Modal>
            </Flex>
        </Main>
    );
};

export default CheckIn;
