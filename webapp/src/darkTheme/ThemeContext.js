/* eslint-disable react/prop-types */
/* eslint-disable arrow-parens */
/* eslint-disable arrow-body-style */
/* eslint-disable react/jsx-props-no-spreading */
import React from 'react';
import styled, { ThemeProvider } from 'styled-components';
import { Switch as Switch2 } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import { backgroundColor, textColor } from './theme';


const ThemeToggleContext = React.createContext();

export const useTheme = () => React.useContext(ThemeToggleContext);
const IOSSwitch = withStyles(theme => ({
  root: {
    width: 42,
    height: 26,
    padding: 0,
    margin: theme.spacing(1),
  },
  switchBase: {
    padding: 1,
    '&$checked': {
      transform: 'translateX(16px)',
      color: theme.palette.common.white,
      '& + $track': {
        backgroundColor: '#060606',
        opacity: 1,
        border: 'none',
      },
    },
    '&$focusVisible $thumb': {
      color: '#060606',
      border: '6px solid #fff',
    },
  },
  thumb: {
    width: 24,
    height: 24,
  },
  track: {
    borderRadius: 26 / 2,
    border: `1px solid ${theme.palette.grey[400]}`,
    backgroundColor: theme.palette.grey[50],
    opacity: 1,
    transition: theme.transitions.create(['background-color', 'border']),
  },
  checked: {},
  focusVisible: {},
}))(({ classes, ...props }) => {
  return (
    <Switch2
      focusVisibleClassName={classes.focusVisible}
      disableRipple
      classes={{
        root: classes.root,
        switchBase: classes.switchBase,
        thumb: classes.thumb,
        track: classes.track,
        checked: classes.checked,
      }}
      {...props}
    />
  );
});

export const MyThemeProvider = ({ children }) => {
  const [themeState, setThemeState] = React.useState({
    mode: 'light',
    checkedB: true,

  });

  const Wrapper = styled.div`
    background-color: ${backgroundColor};
    color: ${textColor};
  `;

  const toggle = name => event => {
    const mode = (themeState.mode === 'light' ? 'dark' : 'light');
    setThemeState({ mode, [name]: event.target.checked });
  };

  return (
    <ThemeToggleContext.Provider value={{ toggle }}>
      <ThemeProvider
        theme={{
          mode: themeState.mode,
        }}
      >
        <Wrapper>
          <IOSSwitch
            checked={themeState.checkedB}
            onChange={toggle('checkedB')}
            value="checkedB"
          />
          {children}
        </Wrapper>
      </ThemeProvider>
    </ThemeToggleContext.Provider>
  );
};

export default MyThemeProvider;
