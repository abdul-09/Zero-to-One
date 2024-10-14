import React from "react";
import { useForm } from "react-hook-form";
import { AuthActions } from "@/app/auth/utils";
import { FaAddressCard, FaRegEnvelope } from "react-icons/fa";
import { MdLockOutline } from "react-icons/md";
import { useRouter } from "next/navigation";
import Image from "next/image";
import logo from "@/app/Klima360LG.png"

type FormData = {
  email: string;
  full_name: string;
  password: string;
  confirm_password: string;
};

const Register = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<FormData>();

  const router = useRouter();

  const { register: registerUser } = AuthActions(); // Note: Renamed to avoid naming conflict with useForm's register

  const onSubmit = (data: FormData) => {
    registerUser(data.email, data.full_name, data.password, data.confirm_password)
      .json(() => {
        router.push("/");
      })
      .catch(async (error) => {
        if (error.response) {
          try {
            const response = await error.response.json();
            setError("root", {
              type: "manual",
              message: response.detail || "An error occurred during registration.",
            });
          } catch (jsonError) {
            console.error("Error parsing error response:", jsonError);
            setError("root", {
              type: "manual",
              message: "An error occurred during registration.",
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
  return <div className="flex items-center bg-green-200 justify-center min-h-screen py-2">
        <main className="flex items-center justify-center w-full flex-1 px-20 text-center">
            <div className="bg-white rounded-2xl shadow-2xl max-w-4xl">
                <div className="p-7">
                    <div className="text-left font-bold">
                        <span className="text-green-600">
                            <Image src={logo} alt="Company logo" width={120} height={120} placeholder="blur"/>
                        </span>
                    </div>
                    <form id="registerForm" onSubmit={handleSubmit(onSubmit)}>
                    <div className="py-5">
                        <h2 className="text-3xl font-bold text-green-500 mb-2 items-center justify-center">
                            <span className="text-green-800">Register</span> New Account
                        </h2>
                        <div className="border-2 w-10 border-green-600 inline-block mb-2"></div>
                        <div className="flex justify-center my-2">
                        </div>
                        <p className="text-gray-400 my-3">Fill In the Form Below</p>
                        <div className="flex flex-col items-center">
                        <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <FaAddressCard className="text-gray-400 mr-2" />
                                <input type="text" placeholder="Full Names" 
                                className="bg-gray-100 outline-none text-sm flex-1" 
                                {...register("full_name", { required: "full names is required" })}/>
                                {errors.full_name && (<span className="text-xs text-red-600">{errors.full_name.message}</span>
            )}
                            </div>
                           
                            <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <FaRegEnvelope className="text-gray-400 mr-2" />
                                <input type="email" placeholder="Email Address" 
                                className="bg-gray-100 outline-none text-sm flex-1"
                                {...register("email", { required: "Email is required" })}/>
                                {errors.email && (<span className="text-xs text-red-600">{errors.email.message}</span>
            )}
                            </div>
                           
                            
                            <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <MdLockOutline className="text-gray-400 mr-2" />
                                <input type="password" placeholder="your password" 
                                className="bg-gray-100 outline-none text-sm flex-1" 
                                {...register("password", { required: "password is required" })}/>
                               {errors.password && ( <span className="text-xs text-red-600"> {errors.password.message}</span>)} 
                            </div>
                            
                            <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <MdLockOutline className="text-gray-400 mr-2" />
                                <input type="password" placeholder="Confirm Password" 
                                className="bg-gray-100 outline-none text-sm flex-1" 
                                {...register("confirm_password", { required: "confirm Password is required" })}/>
                                
                            </div>
                           

                            <div className="flex justify-between w-64 mb-5">
                                <label className="flex items-center text-xs"><input type="checkbox" 
                                name="remember" className="mr-1 font-sans"/>Remember Me</label>
                            </div>
                            <button className="border-2 border-green-600 rounded-full px-8 py-2 inline-block font-semibold hover:bg-green-600
                                 hover:text-white">Register
                            </button>
                        </div>
                    </div>
                    {errors.root && (
            <span className="text-xs text-red-600">{errors.root.message}</span>
          )}
                    </form>
                </div>
                
            </div>
        </main>
    </div>

};

export default Register;