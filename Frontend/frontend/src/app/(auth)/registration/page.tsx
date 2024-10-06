import Link from "next/link";
import { FaGoogle, FaRegEnvelope } from "react-icons/fa";
import { MdLockOutline } from "react-icons/md";

export default function Registration (){
    return <div className="flex flex-col items-center justify-center min-h-screen py-2">
        <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
            <div className="bg-white rounded-2xl shadow-2xl flex w-2/3 max-w-4xl">
                <div className="w-3/5 p-5">
                    <div className="text-left font-bold">
                        <span className="text-green-600">Company Logo</span>
                    </div>
                    
                    <div className="py-10">
                        <h2 className="text-3xl font-bold text-green-600 mb-2">
                            Sign in to Account
                        </h2>
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
                                <input type="email" name="email" placeholder="Email Address" 
                                className="bg-gray-100 outline-none text-sm flex-1" />
                            </div>
                            <div className="bg-gray-100 w-64 p-2 flex items-center mb-3">
                                <MdLockOutline className="text-gray-400 mr-2" />
                                <input type="password" name="password" placeholder="your password" 
                                className="bg-gray-100 outline-none text-sm flex-1" />
                            </div>
                            <div className="flex justify-between w-64 mb-5">
                                <label className="flex items-center text-xs"><input type="checkbox" 
                                name="remember" className="mr-1"/>Remember Me</label>
                                <Link href="#" className="text-xs">Forgot Password</Link>
                            </div>
                            <Link href="#" className="border-2 border-green-600 rounded-full px-12 py-2 inline-block font-semibold hover:bg-green-600
                                 hover:text-white">Login
                            </Link>
                        </div>
                    </div>
                </div>
                
                <div className="w-2/5 bg-green-700 text-white rounded-tr-2xl rounded-br-2xl py-36 px-12">
                    <h2 className="text-3xl font-bold mb-2">Welcome to Zero-to-One</h2>
                    <div className="border-2 w-10 border-white inline-block mb-2"></div>
                    <p className="mb-2">Fill up your Details and start the journey with Us.</p>
                    <Link href="#" className="border-2 border-white rounded-full px-12 py-2 inline-block font-semibold hover:bg-white
                        hover:text-green-600">Sign Up
                    </Link>
                </div>
            </div>
        </main>
    </div>
}