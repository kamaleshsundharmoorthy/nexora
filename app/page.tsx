import { Metadata } from 'next';
import HomeClient from "@/components/HomeClient";

export const metadata: Metadata = {
  title: 'Nexora',
};

export default function Home() {
  return (
    <HomeClient/>
  );
}
