// src/App.js
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);

  const { getRootProps, getInputProps } = useDropzone({
    accept: 'image/*',
    onDrop: (acceptedFiles) => {
      const newFiles = acceptedFiles.map(file => Object.assign(file, {
        preview: URL.createObjectURL(file)
      }));
      setFiles(prevFiles => [...prevFiles, ...newFiles]);
    }
  });

  // Function to remove a specific image
  const removeImage = (file) => {
    setFiles(prevFiles => prevFiles.filter(f => f !== file));
  };

  // Function to handle image submission to an API
  const submitImagesToAPI = async () => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      setLoading(true);
      const response = await axios.post('https://your-api-endpoint.com/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      setRecipes(response.data.recipes); // Assume API returns recipes
      setLoading(false);
    } catch (error) {
      console.error('Error uploading images:', error);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-200 to-blue-400 p-10">
      <div className="max-w-4xl mx-auto bg-white bg-opacity-90 rounded-xl shadow-2xl p-8 mt-16">
        {/* Title */}
        <h1 className="text-5xl font-extrabold text-gray-800 mb-10 text-center">
          Recipe Finder
        </h1>

        {/* Drag and Drop Area */}
        <div
          {...getRootProps()}
          className="border-4 border-dashed border-blue-400 rounded-2xl h-64 flex justify-center items-center bg-gradient-to-r from-blue-300 to-blue-500 hover:from-blue-400 hover:to-blue-600 cursor-pointer mb-10"
        >
          <input {...getInputProps()} />
          <p className="text-2xl text-gray-700 font-light">Drag & drop your ingredient images here</p>
        </div>

        {/* Display added images */}
        {files.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            {files.map((file, index) => (
              <div key={index} className="relative h-40 w-full overflow-hidden rounded-xl shadow-md">
                <img
                  src={file.preview}
                  alt={file.name}
                  className="h-full w-full object-cover"
                />
                {/* Remove button */}
                <button
                  className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2"
                  onClick={() => removeImage(file)}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Submit Button */}
        {files.length > 0 && (
          <div className="flex justify-center mb-10">
            <button
              onClick={submitImagesToAPI}
              className="bg-blue-600 text-white py-2 px-6 rounded-full text-xl hover:bg-blue-700 focus:outline-none"
            >
              Submit
            </button>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && (
          <div className="flex justify-center mb-10">
            <div className="loader ease-linear rounded-full border-8 border-t-8 border-blue-200 h-24 w-24"></div>
          </div>
        )}

        {/* Recipes */}
        {recipes.length > 0 && (
          <div>
            <h2 className="text-3xl font-semibold text-blue-700 mb-6">Recipes you can make:</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {recipes.map((recipe, index) => (
                <div key={index} className="bg-gradient-to-r from-blue-100 to-blue-200 rounded-2xl p-6 shadow-lg">
                  <img
                    src={recipe.image}
                    alt={recipe.title}
                    className="h-48 w-full object-cover rounded-lg mb-4"
                  />
                  <h3 className="text-2xl font-semibold text-blue-800 mb-2">{recipe.title}</h3>
                  <p className="text-blue-600 text-lg">{recipe.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
