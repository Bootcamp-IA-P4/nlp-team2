export const mockToxicityData = {
  overall: {
    totalComments: 2847,
    toxicComments: 342,
    toxicityRate: 12.0,
    videoTitle: "Sample YouTube Video",
    videoId: "dQw4w9WgXcQ"
  },
  toxicityTypes: [
    { name: 'Abusive', count: 145, percentage: 42.4, color: '#ef4444' },
    { name: 'Hate Speech', count: 89, percentage: 26.0, color: '#f97316' },
    { name: 'Threat', count: 67, percentage: 19.6, color: '#eab308' },
    { name: 'Obscene', count: 45, percentage: 13.2, color: '#8b5cf6' },
    { name: 'Sexist', count: 32, percentage: 9.4, color: '#ec4899' },
    { name: 'Racist', count: 28, percentage: 8.2, color: '#06b6d4' }
  ],
  timelineData: [
    { time: '0-5min', toxic: 23, clean: 187 },
    { time: '5-10min', toxic: 45, clean: 234 },
    { time: '10-15min', toxic: 67, clean: 298 },
    { time: '15-20min', toxic: 89, clean: 312 },
    { time: '20-25min', toxic: 56, clean: 267 },
    { time: '25-30min', toxic: 34, clean: 189 }
  ],
  recentAnalysis: [
    {
      id: 1,
      videoTitle: "Tech Review 2024",
      date: "2024-12-20",
      toxicityRate: 8.5,
      totalComments: 1250
    },
    {
      id: 2,
      videoTitle: "Gaming Stream Highlights",
      date: "2024-12-19", 
      toxicityRate: 15.2,
      totalComments: 890
    }
  ]
};

export const toxicityGuide = {
  categories: [
    {
      type: "Abusive",
      description: "Lenguaje ofensivo, insultos directos o indirectos hacia personas",
      examples: ["Insultos personales", "Ataques al carácter", "Lenguaje despectivo"],
      severity: "high",
      color: "red"
    },
    {
      type: "Hate Speech", 
      description: "Discurso que promueve odio hacia grupos específicos",
      examples: ["Discriminación por raza", "Intolerancia religiosa", "Xenofobia"],
      severity: "high",
      color: "orange"
    },
    {
      type: "Threat",
      description: "Amenazas de violencia física o daño hacia personas",
      examples: ["Amenazas directas", "Intimidación", "Incitación a la violencia"],
      severity: "critical",
      color: "red"
    },
    {
      type: "Obscene",
      description: "Contenido sexualmente explícito o lenguaje vulgar extremo",
      examples: ["Lenguaje sexual explícito", "Contenido pornográfico", "Vulgaridad excesiva"],
      severity: "medium",
      color: "purple"
    },
    {
      type: "Sexist",
      description: "Discriminación o prejuicio basado en el género",
      examples: ["Estereotipos de género", "Misoginia", "Misandria"],
      severity: "high", 
      color: "pink"
    },
    {
      type: "Racist",
      description: "Discriminación o prejuicio basado en la raza o etnia",
      examples: ["Estereotipos raciales", "Supremacismo", "Discriminación étnica"],
      severity: "critical",
      color: "blue"
    }
  ]
};