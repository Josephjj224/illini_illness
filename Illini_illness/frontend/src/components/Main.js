import {Container} from "@chakra-ui/react";

const Main = ({children, ...props}) => {
    return <Container as="main" flexDir="column" justifyContent="center" centerContent {...props}>
        {children}
    </Container>;
};

export default Main;
