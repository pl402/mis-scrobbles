# Proyecto Análisis de datos: Mis Scrobbles de Last.fm

## Introducción

Los datos que se utilizaron para este proyecto fueron recolectados desde
el 28 de enero de 2009 hasta el 27 de enero de 2023, a travez
[Last.fm](https://www.last.fm/es), servicio en el que entre otras cosas
se puede llevar un registro de las canciones escuchadas a travez de los
diferentes conectores para lo que deniomina “scrobbling”, es decir,
cuando se escucha una canción en un dispositivo conectado.

De manera quizas un poco intermitente, se ha llevado un registro de las
canciones escuchadas en los diferentes reproductores web, celular,
estritorio, etc.

El presente proyecto se enfoca en el análisis de los datos recolectados,
con el fin de conocer un poco más sobre las canciones que se escuchan,
así como los artistas que se escuchan.

---

## Instalación de paquetes

```r
install.packages("dplyr")
install.packages("tidyverse")
install.packages("lubridate")
install.packages("ggplot2")
install.packages("ggdark")
```

Cargamos los paquetes:

```r
library(dplyr)
library(tidyverse)
library(lubridate)
library(ggplot2)
library(ggdark)
```

---

## Carga de datos

```r
datos <- read.csv("pl402_limpio.csv", header = TRUE)
```

---

## Limpieza de datos

Cabe mencionar que los datos ya fueron limpiados previamente por un
script de python, en el que sobre todo se convirtio las fechas en fechas
con formato correcto, así como poner en la hora correcta, dicho script
se encuentra en el archivo [limpiaFecha.py](limpiaFecha.py). Los datos
resultantes de este script se encuentran en el archivo
[pl402_limpio.csv](pl402_limpio.csv). Los datos originales en el archivo
[pl402.csv](pl402.csv).

Por lo que solo se realizará una limpieza básica.

Muestra los datos:

```r
head(datos)
```

    ##            Artist                         Album                            Song
    ## 1 Ximena Sariñana         No Todo Lo Puedes Dar   Sin Ti No Puede Estar Tan Mal
    ## 2        Caloncho               Bésame Morenita                 Bésame Morenita
    ## 3    Little Jesus                  Disco de Oro                Gracias por Nada
    ## 4          Sabino                        Guapa! Guapa! (con Charles Ans y Slim)
    ## 5             Zoé MTV Unplugged Música De Fondo             Labios Rotos (Live)
    ## 6        Caloncho                      Buen Pez             Naranjita sí carnal
    ##         Date  Time
    ## 1 2023-02-27 15:28
    ## 2 2023-02-27 15:26
    ## 3 2023-02-27 15:21
    ## 4 2023-02-27 15:16
    ## 5 2023-02-27 15:12
    ## 6 2023-02-27 15:09

Convertir la fecha a formato fecha:

```r
datos$Date <- as.Date(datos$Date, format = "%Y-%m-%d")
```

Convierte la columna “Time” a formato de tiempo:

```r
datos$Time <- as.POSIXct(datos$Time, format = "%H:%M")
```

Elimina los registros que no tengan valores en la columna “Song”:

```r
datos <- datos[!is.na(datos$Song), ]
```

---

## Análisis de datos

Realmente no he podido hacer un analisis de datos enfocado en una
pregunta en particular, ya que no he podido encontrar una pregunta que
me interese, por lo que solo he hecho un analisis de datos básico, con
el fin de conocer un poco más los datos y mostrar algunas gráficas.

### Frecuencia de reproducciones por año:

```r
datos %>%
  mutate(Year = year(Date)) %>%
  count(Year) %>%
  ggplot(aes(x = Year, y = n, fill = Year)) +
  geom_col() +
  geom_text(aes(label = n)) +
  dark_theme_gray() +
  labs(
    title = "Frecuencia de reproducciones por año",
    x = "Año",
    y = "Frecuencia"
  )
```

![](README_files/figure-gfm/Grafica%20Frecuencia%20de%20reproducciones%20por%20año-1.png)<!-- -->

Se puede observar que en un principio era mas constante la frecuencia de
reproducciones, aunque hay una caida drastica existen algunos repuntes
como en 2016, tambien es importante notar que en algun punto de 2017
comence a escuchar más podcast que música, por lo que la frecuencia de
reproducciones de música disminuyo.

### Grafica Top 10 Artistas:

Se guarda en una nueva variable el top 10 de artistas:

```r
top10 <- datos %>%
  count(Artist) %>%
  arrange(desc(n)) %>%
  head(10)
```

Se grafica el top 10 de artistas, separados por año:

```r
datos %>%
  mutate(Year = year(Date)) %>%
  count(Artist, Year) %>%
  filter(Artist %in% top10$Artist) %>%
  ggplot(aes(x = Artist, y = n, fill = Year)) +
  geom_col() +
  coord_flip() +
  dark_theme_gray() +
  labs(
    title = "Top 10 Artistas",
    x = "Año",
    y = "Frecuencia"
  )
```

![](README_files/figure-gfm/Grafica%20Top%2010%20Artistas-1.png)<!-- -->

En esta grafica se puede observa en color mas oscuro las reproducciones
mas viejas y en colores más claros las reproducciones mas recientes. Por
ejemplo **The Beatles** tubieron una mayor frecuencia al inicio,
mientras que **Gorillaz** tiene una mayor frecuenca al final.

### Grafica Top 10 Canciones:

Se guarda en una nueva variable el top 10 de canciones:

```r
top10 <- datos %>%
  count(Song) %>%
  arrange(desc(n)) %>%
  head(10)
```

Se grafica el top 10 de canciones, separados por año:

```r
datos %>%
  mutate(Year = year(Date)) %>%
  count(Song, Year) %>%
  filter(Song %in% top10$Song) %>%
  ggplot(aes(x = Song, y = n, fill = Year)) +
  geom_col() +
  coord_flip() +
  dark_theme_gray() +
  labs(
    title = "Top 10 Canciones",
    x = "Año",
    y = "Frecuencia"
  )
```

![](README_files/figure-gfm/Grafica%20Top%2010%20Canciones-1.png)<!-- -->

De igual menera que en la grafica anterior, aquí se observa que por
ejemplo **Spaceman** de **The Killers** fue escuchada mas al inicio,
**Do I Wanna Know** de **Arctic Monkeys** fue escuchada mas al final.
Esto quizas se deba a que **Do I Wanna Know** es mas reciente que
**Spaceman**.

### Grafica de freuencia de reproducciones por mes:

```r
datos %>%
  mutate(Year = year(Date)) %>%
  mutate(Month = month(Date)) %>%
  mutate(Month = factor(Month,
    levels = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
    labels = c(
      "Enero", "Febrero", "Marzo",
      "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre",
      "Octubre", "Noviembre", "Diciembre"
    )
  )) %>%
  count(Year, Month) %>%
  ggplot(aes(x = Month, y = n, fill = Year)) +
  geom_col() +
  dark_theme_gray() +
  labs(
    title = "Reproducciones por mes",
    x = "Mes",
    y = "Frecuencia"
  )
```

![](README_files/figure-gfm/Grafica%20de%20Reproducciones%20por%20mes-1.png)<!-- -->

Esta grafica esta un poco por todos lados, no se alcanza a percibir
alguna incliniación en los meses, Salvo enero, a pesar de tener menos
reproducciones en general, se nota mas claro, lo que indica mayor
frecuencia de reproducciones en enero los ultimos años.

### Grafica de freuencia de reproducciones por hora:

```r
datos %>%
  mutate(Year = year(Date)) %>%
  mutate(Hour = hour(Time)) %>%
  count(Year, Hour) %>%
  ggplot(aes(x = Hour, y = n, fill = Year)) +
  geom_col() +
  dark_theme_gray() +
  labs(
    title = "Reproducciones por hora",
    x = "Hora",
    y = "Frecuencia"
  )
```

![](README_files/figure-gfm/Grafica%20de%20Reproducciones%20por%20hora-1.png)<!-- -->

Se puede observar que la frecuencia de reproducciones es mas constante a
lo largo del dia, con picos cerca de las 13:00 y 18:00, lo que indica
que es cuando mas escucho musica.

Tambien se observa que los primeros años solía escuchar musica en la
madrugada, cuando aun era estudiante y tenia que hacer trabajos o
estudiar, despues, se observa una mayor frecuenca en horario de oficina
(9:00 - 18:00), cuando inicie a trabajar.

### Grafica de freuencia de reproducciones por dia de la semana:

```r
datos %>%
  mutate(Year = year(Date)) %>%
  mutate(Day = wday(Date)) %>%
  count(Year, Day) %>%
  mutate(Day = factor(Day,
    levels = c(1, 2, 3, 4, 5, 6, 7),
    labels = c(
      "Lunes", "Martes", "Miercoles",
      "Jueves", "Viernes", "Sabado",
      "Domingo"
    )
  )) %>%
  ggplot(aes(x = Day, y = n, fill = Year)) +
  geom_col() +
  dark_theme_gray() +
  labs(
    title = "Reproducciones por dia de la semana",
    x = "Año",
    y = "Dia"
  )
```

![](README_files/figure-gfm/Grafica%20de%20Reproducciones%20por%20dia%20de%20la%20semana-1.png)<!-- -->

La grafica parece dibujar una distribucion estandar, donde el punto mas
alto es el día miercoles. Tambien se observa una inclinación por
escuchar musica los lunes en los ultimos años.

### Grafica de un heat map de la frecuenca por año y mes:

```r
datos %>%
  mutate(Year = year(Date)) %>%
  mutate(Month = month(Date)) %>%
  count(Year, Month) %>%
  mutate(Month = factor(Month,
    levels = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
    labels = c(
      "Enero", "Febrero", "Marzo",
      "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre",
      "Octubre", "Noviembre", "Diciembre"
    )
  )) %>%
  ggplot(aes(x = Year, y = Month, fill = n)) +
  geom_tile() +
  dark_theme_gray() +
  labs(
    title = "Reproducciones por año y mes",
    x = "Año",
    y = "Mes"
  )
```

![](README_files/figure-gfm/Grafica%20de%20Reproducciones%20por%20año%20y%20mes-1.png)<!-- -->

De nuevo, se observa que la frecuencia era mayor al inicio, y disminuye
al final. Incluso hay meses en los que no se escucharon canciones,
probablemente por no configurar correctamente el conectro de last.fm.

## Conclusiones

- En general, se observa que la frecuencia de reproducciones es mayor
  al inicio, y disminuye al final.

- Mi top 10 de artistas son artistas que he escuchado desde hace mucho
  tiempo, no parece haber artistas nuevos aunque algunos los escuche
  más los ultimos años.

- Igualmente con las canciones, las que mas escucho las he escuchado
  desde un principio, por lo menos de estos registros.

- Hay alguna inclinación a escuchar musica los miercoles, pero no es
  muy marcada. Los lunes casi no hay reproducciones, pero los ultimos
  años se ha incrementado.

- La frecuencia de reproducciones es mas constante a lo largo del dia,
  con picos cerca de las 13:00 y 18:00, lo que indica que es cuando
  mas escucho musica.

- Fue un ejercicio interesante, aunque no se pudo obtener mucha
  información, ya que no se puedo obtener los datos de las canciones
  que se escucharon, solo los artistas y las fechas, sería interesante
  poder obtener los datos de las canciones, como el genero, duración,
  tema general de la canción, BPM, entre otros, para poder hacer un
  análisis mas profundo.

## Referencias

- [Last.fm API](https://www.last.fm)

- R Core Team (2022). R: A language and environment for statistical
  computing. R Foundation for Statistical Computing, Vienna, Austria.
  URL <https://www.R-project.org/>.

- Package Version 1.2.1.
  <https://CRAN.R-project.org/package=tidyverse>

- The R Graph Gallery (2021). The R Graph Gallery.
  <https://www.r-graph-gallery.com/>

- Coursera (2021). Análisis de Datos de Google.
  <https://www.coursera.org/professional-certificates/analisis-de-datos-de-google>
