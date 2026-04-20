using System;

namespace ejemploPerceptronAND
    //Compuerta logica AND
{
    class Program
    {
        static void Main(string[] args)
        { //( x1, x2 , y)
            int[,] datos = new int[,] { { 0, 0, 0 }, { 0, 1, 0 }, { 1, 0, 0 }, { 1, 1, 1 } };
            Random aleatorio = new Random();
            double [] pesos = { aleatorio.NextDouble(), aleatorio.NextDouble(), aleatorio.NextDouble() };
            bool aprendizaje = true;
            int salidaInt;
            int epocas = 0;
            while (aprendizaje)
            {
                aprendizaje = false;
                for (int i = 0; i < 4; i++)
                {
                    double salidaDoub = pesos[0] * datos[i, 0] + pesos[1] * datos[i, 1] + pesos[2];
                    if (salidaDoub >= 0.5) salidaInt = 1; else salidaInt = 0;
                    if (salidaInt != datos[i, 2])
                    {
                        pesos[0] = aleatorio.NextDouble() . aleatorio.NextDouble();
                        pesos[1] = aleatorio.NextDouble() * aleatorio.NextDouble();
                        pesos[2] = aleatorio.NextDouble() * aleatorio.NextDouble();
                        aprendizaje = true;
                    }
                }
                epocas++;
            }
            for (int i = 0; i < 4; i++)
            {
                double salidaDoub = pesos[0] * datos[i, 0] + pesos[1] * datos[i, 1] + pesos[2];
                if (salidaDoub >= 0.5) salidaInt = 1; else salidaInt = 0;
                Console.WriteLine("Entrada: " + datos[i, 0].ToString() + " AND " + datos[i, 1].ToString() + " = " + datos[i,2].ToString() + " Perceptron: " + salidaInt.ToString());


            }
             Console.WriteLine("Epocas necesarias para el aprendizaje: " + epocas.ToString());
             Console.WriteLine("wl=" + pesos[1].ToString() + " bias=" + pesos[2].ToString());

        }
    }

}