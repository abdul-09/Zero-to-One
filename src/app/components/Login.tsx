import React from "react";
import { useForm } from "react-hook-form";
import { AuthActions } from "@/app/auth/utils";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { FaGoogle, FaRegEnvelope } from "react-icons/fa";
import { MdLockOutline } from "react-icons/md";
import Image from "next/image";
import logo from "@/app/Klima360LG.png";
type FormData = {
  email: string;
  password: string;
};

const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<FormData>();

  const router = useRouter();

  const { login, storeToken } = AuthActions();

  const onSubmit = (data: FormData) => {
    login(data.email, data.password)
      .json((json) => {
        storeToken(json.access, "access");
        storeToken(json.refresh, "refresh");

        router.push("dashboard");
      })
      .catch(async (error) => {
        if (error.response) {
          try {
            const response = await error.response.json();
            setError("root", {
              type: "manual",
              message: response.detail || "An error occurred during login.",
            });
          } catch (jsonError) {
            console.error("Error parsing error response:", jsonError);
            setError("root", {
              type: "manual",
              message: "An error occurred during login.",
            });
          }
        } else {
          // Handle other error types (e.g., network errors, timeout errors)
          console.error("Network error:", error);
          setError("root", {
            type: "manual",
            message: "Network error. Please try again later.",
          });
        }
      });
  };
  return <div className="flex flex-col items-center  bg-green-200 justify-center min-h-screen py-2">
  <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
      <div className="bg-white rounded-2xl shadow-2xl flex w-2/3 max-w-4xl">
          <div className="w-3/5 p-5">
              <div className="text-left font-bold">
                  <span className="text-green-600">
                      <Image src={logo} alt="Company logo" width={120} height={120} placeholder="blur"/>
                  </span>
              </div>
              
              <div className="py-10">
                  <h2 className="text-3xl font-bold text-green-600 mb-2">
                      Sign in to Account
                  </h2>
                  <form onSubmit={handleSubmit(onSubmit)}>
                  <div className="border-2 w-10 border-green-600 inline-block mb-2"></div>
                  <div className="flex justify-center my-2">
                      <Link href="#" className="border-2 border-gray-200 rounded-full p-3 mx-1">
                          <FaGoogle className="text-sm" />
                      </Link>
                  </div>
                  <p className="text-gray-400 my-3">Or You Use Your Account</p>
                  <div className="flex flex-col items-center">
                      <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                          <FaRegEnvelope className="text-gray-400 mr-2" />
                          <input type="email" placeholder="Email Address" 
                          {...register("email", { required: true })}
                          className="bg-gray-100 outline-none text-sm flex-1" />
                          {errors.email && (
                            <span className="text-xs text-red-600">Email is required</span>
                            )}
                      </div>
                      <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                          <MdLockOutline className="text-gray-400 mr-2" />
                          <input type="password" placeholder="your password"
                          {...register("password", { required: true })} 
                          className="bg-gray-100 outline-none text-sm flex-1" />
                          {errors.password && (
                            <span className="text-xs text-red-600">Password is required</span>
                            )}
                      </div>
                      <div className="flex justify-between w-64 mb-5">
                          <label className="flex items-center text-xs"><input type="checkbox" 
                          name="remember" className="mr-1 font-sans"/>Remember Me</label>
                          <Link href="/auth/password/reset-password" className="text-xs">Forgot Password</Link>
                      </div>
                      <button className="border-2 border-green-600 rounded-full px-10 py-2 inline-block font-semibold hover:bg-green-600
                           hover:text-white">Login
                      </button>
                  </div>
                  </form>
              </div>
              
          </div>
          
          <div className="w-2/5 bg-green-700 text-white rounded-tr-2xl rounded-br-2xl py-36 px-12">
              <h2 className="text-3xl font-bold mb-2">Welcome to Zero-to-One</h2>
              <div className="border-2 w-10 border-white inline-block mb-2"></div>
              <p className="mb-2">Create an account and start the journey with Us.</p>
              <Link href="/auth/register" className="border-2 border-white rounded-full px-8 py-2 inline-block font-semibold hover:bg-white
                  hover:text-green-600">Sign Up
              </Link>
          </div>
      </div>
  </main>
</div>

};

export default Login;
