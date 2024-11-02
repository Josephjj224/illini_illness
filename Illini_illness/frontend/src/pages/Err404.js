import Main from "../components/Main.js";
import {useNavigate} from "react-router-dom";
import {Box, Button, Heading, Text} from "@chakra-ui/react";
import {ArrowBackIcon} from "@chakra-ui/icons";

const Err404 = () => {
    const nav = useNavigate();

	return <Main>
        <Heading as="h2" size="3xl">404</Heading>
        <Button
            onClick={() => nav(-1)}
            leftIcon={<ArrowBackIcon />}
            variant="ghost"
            size="md"
            // colorScheme="navy"
            mt="4"
        >
            Page not found
        </Button>
    </Main>;
};

export default Err404;
