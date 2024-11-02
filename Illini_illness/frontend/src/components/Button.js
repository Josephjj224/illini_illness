import {Button} from "@chakra-ui/react";

const ColorButton = ({colorScheme, children, variant, ...props}) => {
	return variant ?
        <Button
            variant={variant}
            borderWidth={variant === "outline" ? "2px" : null}
            colorScheme={colorScheme}
            color={colorScheme + ".500"}
            {...props}
        >
            {children}
        </Button>
    :
        <Button
            backgroundColor={colorScheme + ".500"}
            color="whiteAlpha.900"
            // borderRadius="300"
            _hover={{bg: colorScheme + ".600"}}
            {...props}
        >
            {children}
        </Button>;
};

export default ColorButton;
