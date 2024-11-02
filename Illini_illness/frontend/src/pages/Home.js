import {useEffect} from "react";
import {Heading, Text, Stack} from "@chakra-ui/react";
import {Link, useNavigate} from "react-router-dom";

import Main from "../components/Main";
import Button from "../components/Button";
import useAuth from "../hooks/useAuth";

const Home = () => {
    const nav = useNavigate();
    const {userID} = useAuth();
    const buttonStyles = {px: 8, flex: 1, mt: 8, colorScheme: "red"};

    useEffect(() => {
        document.title = "Illini Illness";

        // if (userID) {
        //     nav("/dashboard");
        // }
    }, [userID]);

	return <Main>
        <Heading as="h1" size="3xl" mb="4">Illini Illness</Heading>
        <Text>Track and manage your symptoms</Text>
        <Stack direction="row" gap="6">
            <Button as={Link} to="/register" {...buttonStyles}>Register</Button>
            <Button as={Link} to="/login" {...buttonStyles}>Log In</Button>
        </Stack>
    </Main>;
};

export default Home;
