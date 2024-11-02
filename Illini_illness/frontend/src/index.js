import {ColorModeScript} from '@chakra-ui/react';
import React, {StrictMode} from 'react';
import * as ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';
import * as serviceWorker from './serviceWorker';
import {BrowserRouter} from "react-router-dom";
import {ChakraProvider, extendTheme} from '@chakra-ui/react'; // extendTheme
import {mode} from '@chakra-ui/theme-tools';

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);

// change input colors on dark mode to preserve high saturation
// add floating input
const theme = extendTheme({
    colors: {
        red: {200: "#e53e3e", 300: "#e53e3e"},
        blue: {200: "#3182ce", 300: "#3182ce"},
        green: {200: "#38a169", 300: "#38a169"},
    },
    components: {
        Form: {
            variants: {
                floating: {
                    container: {
                        label: {
                            top: "-.75em",
                            left: 0,
                            zIndex: 2,
                            position: "absolute",
                            backgroundColor: "white",
                            pointerEvents: "none",
                            mx: 2,
                            px: 2,
                            fontSize: ".8em"
                        }
                    }
                }
            }
        }
    }
})

root.render(
    <StrictMode>
        <ColorModeScript />
        <BrowserRouter>
            <ChakraProvider theme={theme}>
                <App />
            </ChakraProvider>
        </BrowserRouter>
    </StrictMode>
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorker.unregister();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
