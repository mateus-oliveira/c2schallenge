import React, { useState } from 'react';
import { View, Text, TextInput, Button, FlatList, Image, StyleSheet } from 'react-native';
import axios from 'axios';

export default function App() {
  const [sentence, setSentence] = useState('');
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `http://localhost:8000/cars/ai?sentence=${encodeURIComponent(sentence)}`
      );
      setCars(response.data);
    } catch (error) {
      console.error('Erro ao buscar carros:', error.message);
      alert('Erro ao buscar carros');
    } finally {
      setLoading(false);
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <Image source={{ uri: item.image }} style={styles.image} />
      <View style={styles.info}>
        <Text style={styles.title}>{item.brand} {item.model} ({item.year})</Text>
        <Text style={styles.details}>Cor: {item.color}</Text>
        <Text style={styles.details}>Motor: {item.engine} - {item.fuel}</Text>
        <Text style={styles.details}>Km: {item.mileage.toLocaleString()} km</Text>
        <Text style={styles.details}>Transmissão: {item.transmission}</Text>
        <Text style={styles.details}>Portas: {item.doors}</Text>
        <Text style={styles.price}>R$ {item.price.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.header}>C2S - Cars to Sale</Text>
      <TextInput
        style={styles.input}
        placeholder="Informe os detalhes do veículo que está procurando"
        value={sentence}
        onChangeText={setSentence}
      />
      <Button title={loading ? "Buscando..." : "Buscar"} onPress={handleSearch} disabled={loading} />

      <FlatList
        data={cars}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 60,
    paddingHorizontal: 16,
    backgroundColor: '#f2f2f2',
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    height: 50,
    backgroundColor: '#fff',
    borderRadius: 8,
    paddingHorizontal: 16,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  list: {
    paddingTop: 20,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 8,
    marginBottom: 20,
    overflow: 'hidden',
    elevation: 3,
  },
  image: {
    width: '100%',
    height: 180,
  },
  info: {
    padding: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 6,
  },
  details: {
    fontSize: 14,
    color: '#555',
    marginBottom: 2,
  },
  price: {
    fontSize: 18,
    color: '#2e7d32',
    fontWeight: 'bold',
    marginTop: 10,
  },
});
