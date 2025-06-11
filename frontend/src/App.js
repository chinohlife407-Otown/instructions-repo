import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

export default function App() {
  const [city, setCity] = useState('');
  const [businessType, setBusinessType] = useState('');
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);

  const runScraper = async () => {
    setLoading(true);
    try {
      const res = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/scraper/run_all`,
        { params: { city, business_type: businessType } }
      );
      const allLeads = [
        ...res.data.linkedin,
        ...res.data.zillow,
        ...res.data.businesses,
      ];
      setLeads(allLeads);
    } catch (err) {
      alert('Something broke. Probably LinkedIn.');
    }
    setLoading(false);
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">LeadGen Master Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <input
          type="text"
          placeholder="City"
          className="p-2 border rounded"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <input
          type="text"
          placeholder="Business Type or Role"
          className="p-2 border rounded"
          value={businessType}
          onChange={(e) => setBusinessType(e.target.value)}
        />
        <button
          onClick={runScraper}
          className="bg-black text-white p-2 rounded hover:bg-gray-800"
        >
          {loading ? 'Scraping...' : 'Run Scraper'}
        </button>
      </div>

      {leads.length > 0 && (
        <table className="w-full text-left border mt-6">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2">Name</th>
              <th className="p-2">Company</th>
              <th className="p-2">City</th>
              <th className="p-2">Contact</th>
              <th className="p-2">Source</th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead, i) => (
              <tr key={i} className="border-t">
                <td className="p-2">{lead.name}</td>
                <td className="p-2">{lead.company}</td>
                <td className="p-2">{lead.city}</td>
                <td className="p-2">{lead.contact}</td>
                <td className="p-2">{lead.source}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
