import {useEffect, useState} from "react";
import React from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from "axios";
import {
    FormControl,
    Input,
    FormLabel,
    InputGroup,
    InputRightElement,
    IconButton,
    Stack,
    Spacer,
    Link as ChakraLink
} from "@chakra-ui/react";
import {IconEye, IconEyeClosed} from "@tabler/icons-react";
import Main from "../components/Main";
import Button from "../components/Button";
import {Link, useNavigate} from "react-router-dom";
import useAuth from "../hooks/useAuth";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const nav = useNavigate();
    const {userID, setUserData} = useState(true);
    //const {userID, setUserData} = useAuth();

    

    const login = async () => {
        console.log("log in", email, password);
        nav("/Dashboard");

        
    }

	return <Main>
        <FormControl variant="floating" maxW="18em">
            <FormLabel>Email</FormLabel>
            <Input
                type="email"
                placeholder="email"
                value={email}
                onChange={(ev) => setEmail(ev.target.value)}
                mb="2"
            />
        </FormControl>
        <FormControl variant="floating" mt="2" maxW="18em">
            <FormLabel>Password</FormLabel>
            <InputGroup mb="2">
                <Input
                    type={showPassword ? "text" : "password"}
                    placeholder="password"
                    value={password}
                    onChange={(ev) => setPassword(ev.target.value)}
                />
                <InputRightElement>
                    <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        icon={showPassword ? <IconEye /> : <IconEyeClosed />}
                        aria-label="show-password"
                        variant="ghost"
                        opacity=".4"
                    />
                </InputRightElement>
            </InputGroup>
        </FormControl>
        <Button onClick={login} width="18em" mt="2" colorScheme="red">Log In</Button>
        <ToastContainer />
        <ChakraLink as={Link} to="/register" mt="6" textDecoration="underline" opacity=".8">New user? Register now</ChakraLink>
    </Main>;
};

export default Login;
