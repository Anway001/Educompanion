import React, { createContext, useState, useContext } from 'react';

const PodcastContext = createContext();

export const usePodcastContext = () => useContext(PodcastContext);

export const PodcastProvider = ({ children }) => {
    const [uploadMode, setUploadMode] = useState('upload');
    const [notes, setNotes] = useState('');
    const [length, setLength] = useState('medium');
    const [podcastUrl, setPodcastUrl] = useState('');
    const [statusMessage, setStatusMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [generatedFilename, setGeneratedFilename] = useState(null);
    // We can't persist File objects easily if the component unmounts in some browsers/cases,
    // but we can try. If 'selectedFiles' clears on nav, users usually expect to re-select files anyway.
    // The important part is persisting the *result* (podcastUrl) and *input* (notes).
    const [selectedFiles, setSelectedFiles] = useState([]);

    const value = {
        uploadMode, setUploadMode,
        notes, setNotes,
        length, setLength,
        podcastUrl, setPodcastUrl,
        statusMessage, setStatusMessage,
        isLoading, setIsLoading,
        generatedFilename, setGeneratedFilename,
        selectedFiles, setSelectedFiles
    };

    return (
        <PodcastContext.Provider value={value}>
            {children}
        </PodcastContext.Provider>
    );
};
