// src/app/auth/utils.ts
import wretch from "wretch";
import Cookies from "js-cookie";

// Base API setup for making HTTP requests
const api = wretch("http://localhost:8000").accept("application/json");

const storeToken = (token: string, type: "access" | "refresh") => {
    Cookies.set(type + "Token", token);
  };
  
  /**
   * Retrieves a token from cookies.
   * @param {"access" | "refresh"} type - The type of the token to retrieve (access or refresh).
   * @returns {string | undefined} The token, if found.
   */
  const getToken = (type: string) => {
    return Cookies.get(type + "Token");
  };

  
  /**
   * Removes both access and refresh tokens from cookies.
   */
  const removeTokens = () => {
    Cookies.remove("accessToken");
    Cookies.remove("refreshToken");
  };
  


  const register = (email: string, full_name: string, password: string, confirm_password: string) => {
    return api.post({ email, full_name, password, confirm_password }, "/register/");
  };
  
  const login = (email: string, password: string) => {
    return api.post({ email, password }, "/login/");
  };
  
  const logout = () => {
    const refreshToken = getToken("refresh");
    return api.post({ refresh: refreshToken }, "/logout/");
  };
  
  const handleJWTRefresh = () => {
    const refreshToken = getToken("refresh");
    return api.post({ refresh: refreshToken }, "/token/refresh");
  };
  
  const resetPassword = (email: string) => {
    return api.post({ email }, "/password-reset/");
  };
  
  const resetPasswordConfirm = (
    uid: string,
    token: string,
    new_password: string,
    re_new_password: string
  ) => {
    return api.post(
      { uid, token, new_password, re_new_password},
      "/password-reset-confirm/",
      
    );
  };

  export const AuthActions = () => {
    return {
      login,
      resetPasswordConfirm,
      handleJWTRefresh,
      register,
      resetPassword,
      storeToken,
      getToken,
      logout,
      removeTokens,
    };
  };