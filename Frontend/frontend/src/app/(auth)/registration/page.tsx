'use client'
// import Link from "next/link";
import { useFormState } from "react-dom";
import { FaAddressCard, FaRegEnvelope } from "react-icons/fa";
import { MdLockOutline } from "react-icons/md";
import Image from "next/image";
import logo from "../Klima360LG.png";
// import { useFormState } from "react-dom";
// import { register } from '@/app/lib/actions';
import { registerUserAction } from "@/app/data/actions/auth-actions";

import { ZodErrors } from "@/app/components/custom/zodErrors"

const INITIAL_STATE = {
    data: null, 
};


export default function Registration (){

    const [formState, formAction] = useFormState(registerUserAction, INITIAL_STATE);

    console.log(formState);

    return <div className="flex items-center bg-green-200 justify-center min-h-screen py-2">
        <main className="flex items-center justify-center w-full flex-1 px-20 text-center">
            <div className="bg-white rounded-2xl shadow-2xl max-w-4xl">
                <div className="p-7">
                    <div className="text-left font-bold">
                        <span className="text-green-600">
                            <Image src={logo} alt="Company logo" width={120} height={120} placeholder="blur"/>
                        </span>
                    </div>
                    <form id="registerForm" action={formAction}>
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
                                <input type="text" name="fullnames" placeholder="Full Names" 
                                className="bg-gray-100 outline-none text-sm flex-1" />
                            </div>
                            <ZodErrors error={formState?.zodErrors?.fullnames} />
                            <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <FaRegEnvelope className="text-gray-400 mr-2" />
                                <input type="email" name="email" placeholder="Email Address" 
                                className="bg-gray-100 outline-none text-sm flex-1"/>
                            </div>
                            <ZodErrors error={formState?.zodErrors?.email} />
                            
                            <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <MdLockOutline className="text-gray-400 mr-2" />
                                <input type="password" name="password" placeholder="your password" 
                                className="bg-gray-100 outline-none text-sm flex-1" />
                                
                            </div>
                            <ZodErrors error={formState?.zodErrors?.password} />
                            <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <MdLockOutline className="text-gray-400 mr-2" />
                                <input type="password" name="confirmPassword" placeholder="Confirm Password" 
                                className="bg-gray-100 outline-none text-sm flex-1" />
                                
                            </div>
                            <ZodErrors error={formState?.zodErrors?.confirmPassword} />

                            <div className="flex justify-between w-64 mb-5">
                                <label className="flex items-center text-xs"><input type="checkbox" 
                                name="remember" className="mr-1 font-sans"/>Remember Me</label>
                            </div>
                            <button className="border-2 border-green-600 rounded-full px-12 py-2 inline-block font-semibold hover:bg-green-600
                                 hover:text-white">Register
                            </button>
                        </div>
                    </div>
                    </form>
                </div>
                
                {/* <div className="w-2/5 bg-green-700 text-white rounded-tr-2xl rounded-br-2xl py-36 px-12">
                    <h2 className="text-3xl font-bold mb-2">Welcome to Zero-to-One</h2>
                    <div className="border-2 w-10 border-white inline-block mb-2"></div>
                    <p className="mb-2">Fill up your Details and start the journey with Us.</p>
                    <Link href="#" className="border-2 border-white rounded-full px-12 py-2 inline-block font-semibold hover:bg-white
                        hover:text-green-600">Sign Up
                    </Link>
                </div> */}
            </div>
        </main>
    </div>
}