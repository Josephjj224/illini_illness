import {useState, useEffect} from "react";
import axios from "axios";
import {FormControl, Input, InputGroup, InputRightElement, IconButton, Stack, Spacer, RadioGroup,
    Radio, FormLabel, Select, Box} from "@chakra-ui/react";
import {Link, useNavigate} from "react-router-dom";
import {IconEye, IconEyeClosed} from "@tabler/icons-react";
import PhoneInput from 'react-phone-number-input/input';
import 'react-phone-number-input/style.css';
import Main from "../components/Main";
import Button from "../components/Button";
import "../styles/form.scss";
import useAuth from "../hooks/useAuth";

const Register = () => {
    const [name, setName] = useState(["", ""]);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [phone, setPhone] = useState();
    const [role, setRole] = useState("patient");
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("female");
    const [allDoctors, setAllDoctors] = useState([]);
    const [selectedDoctor, setSelectedDoctor] = useState("");
    const nav = useNavigate();
    const {userID, setUserData} = useAuth();


    useEffect(() => {
        axios.get("http://34.41.122.202:5000/api/doctor-list")
            .then(res => {
                console.log(res.data);
                setAllDoctors(res.data.doctors);
            }).catch(err => console.log(err));
    }, []);

    const register = async () => {
        let data = {email, password, phone, role, firstName: name[0], lastName: name[1]};
        if (role === "patient") {
            data = {...data, age, gender, doctor: selectedDoctor};
        }
        console.log("register", data);
        try {
            const res = await axios.post("http://34.41.122.202:5000/api/register", data);
            console.log(res);
            setUserData(res.data);
        } catch (err) {
            // todo error handling
            console.log(err);
        }
    }

    return <Main>
        <Stack className="register-form" direction="column" gap="8">
            <Stack direction="column">
                <Stack direction="row" mt="2">
                    <FormLabel mb="6">Register as:</FormLabel>
                    <RadioGroup value={role} onChange={setRole}>
                        <Radio value="patient" colorScheme="red" mx="2">Patient</Radio>
                        <Radio value="doctor" colorScheme="red" mx="2">Doctor</Radio>
                    </RadioGroup>
                </Stack>

                <Stack direction={["column", "row"]} width="18em">
                    <FormControl flex="1" variant="floating">
                        <FormLabel>First Name</FormLabel>
                        <Input
                            type="text"
                            placeholder="Jane"
                            value={name[0]}
                            onChange={(ev) => setName([ev.target.value, name[1]])}
                            mb="2"
                        />
                    </FormControl>
                    <FormControl flex="1" variant="floating">
                        <FormLabel>Last Name</FormLabel>
                        <Input
                            type="text"
                            placeholder="Doe"
                            value={name[1]}
                            onChange={(ev) => setName([name[0], ev.target.value])}
                            mb="2"
                        />
                    </FormControl>
                </Stack>

                <FormControl width="18em" variant="floating" mt="2">
                    <FormLabel>Email</FormLabel>
                    <Input
                        type="email"
                        placeholder="janedoe@example.com"
                        value={email}
                        onChange={(ev) => setEmail(ev.target.value)}
                        mb="2"
                    />
                </FormControl>
                <FormControl width="18em" variant="floating" mt="2">
                    <FormLabel>Password</FormLabel>
                    <InputGroup mb="2">
                        <Input
                            type={showPassword ? "text" : "password"}
                            placeholder="********"
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
                <FormControl width="18em" variant="floating" mt="2">
                    <FormLabel>Phone Number</FormLabel>
                    <Input
                        as={PhoneInput}
                        value={phone}
                        onChange={setPhone}
                        defaultCountry="US"
                        // addInternationalOption={false}
                        placeholder="(123) 456-7890"
                    />
                </FormControl>
            </Stack>
            {role === "patient" && <>
                <Stack direction="column">
                    <Stack direction="row" width="18em" mt="4">
                        <FormControl variant="floating">
                            <FormLabel>Age</FormLabel>
                            <Input
                                type="number"
                                placeholder="0"
                                value={age}
                                onChange={ev => setAge(ev.target.value)}
                                mb="2"
                            />
                        </FormControl>
                        <FormControl variant="floating">
                            <FormLabel>Gender</FormLabel>
                            <Select value={gender} onChange={ev => setGender(ev.target.value)}>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </Select>
                        </FormControl>
                    </Stack>
                    <FormControl variant="floating">
                        <FormLabel>Doctor</FormLabel>
                        <Select value={selectedDoctor} onChange={ev => setSelectedDoctor(ev.target.value)}>
                            {allDoctors.map((data, i) =>
                                <option key={i} value={data.docID}>{data.firstName} {data.lastName}</option>
                            )}
                        </Select>
                    </FormControl>
                </Stack>
            </>}
        </Stack>

        <Button
            onClick={register}
            className="register-button"
            width="18em"
            mt="4"
            colorScheme="red"
        >
            Register
        </Button>
    </Main>;
};

export default Register;
