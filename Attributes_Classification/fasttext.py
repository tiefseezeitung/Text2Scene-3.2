{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(27657, 9)\n",
      "(16594, 9)\n",
      "(5531, 9)\n",
      "(5532, 9)\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>iso</th>\n",
       "      <th>dimensionality</th>\n",
       "      <th>form</th>\n",
       "      <th>motion_type</th>\n",
       "      <th>motion_class</th>\n",
       "      <th>motion_sense</th>\n",
       "      <th>semantic_type</th>\n",
       "      <th>motion_signal_type</th>\n",
       "      <th>text</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>Highlights</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>of</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>the</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>Prado</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>Museum</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>27652</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>More</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>27653</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>on</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>27654</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>this</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>27655</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>later</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>27656</th>\n",
       "      <td>__label__O</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>__label__nan</td>\n",
       "      <td>.</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>27657 rows × 9 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "              iso dimensionality          form   motion_type  motion_class  \\\n",
       "0      __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "1      __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "2      __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "3      __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "4      __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "...           ...            ...           ...           ...           ...   \n",
       "27652  __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "27653  __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "27654  __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "27655  __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "27656  __label__O   __label__nan  __label__nan  __label__nan  __label__nan   \n",
       "\n",
       "       motion_sense semantic_type motion_signal_type        text  \n",
       "0      __label__nan  __label__nan       __label__nan  Highlights  \n",
       "1      __label__nan  __label__nan       __label__nan          of  \n",
       "2      __label__nan  __label__nan       __label__nan         the  \n",
       "3      __label__nan  __label__nan       __label__nan       Prado  \n",
       "4      __label__nan  __label__nan       __label__nan      Museum  \n",
       "...             ...           ...                ...         ...  \n",
       "27652  __label__nan  __label__nan       __label__nan        More  \n",
       "27653  __label__nan  __label__nan       __label__nan          on  \n",
       "27654  __label__nan  __label__nan       __label__nan        this  \n",
       "27655  __label__nan  __label__nan       __label__nan       later  \n",
       "27656  __label__nan  __label__nan       __label__nan           .  \n",
       "\n",
       "[27657 rows x 9 columns]"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import pandas as pd \n",
    "import numpy as np\n",
    "\n",
    "\n",
    "df = pd.read_csv(\"train.csv\")\n",
    "df.head()\n",
    "df['iso'] = '__label__' + df['iso'].astype(str)\n",
    "df['dimensionality'] = '__label__' + df['dimensionality'].astype(str)\n",
    "df['form'] = '__label__' + df['form'].astype(str)\n",
    "df['motion_type'] = '__label__' + df['motion_type'].astype(str)\n",
    "df['motion_class'] = '__label__' + df['motion_class'].astype(str)\n",
    "df['motion_sense'] = '__label__' + df['motion_sense'].astype(str)\n",
    "df['semantic_type'] = '__label__' + df['semantic_type'].astype(str)\n",
    "df['motion_signal_type'] = '__label__' + df['motion_signal_type'].astype(str)\n",
    "\n",
    "df = df[['iso', 'dimensionality','form', 'motion_type', 'motion_class', 'motion_sense', 'semantic_type', 'motion_signal_type','text']]\n",
    "train,test,dev = np.split(df,[int(.6*len(df)),int(.8*len(df))])\n",
    "print(df.shape)\n",
    "print(train.shape)\n",
    "print(test.shape)\n",
    "print(dev.shape)\n",
    "train.to_csv(r\"C:\\Users\\anika\\Desktop\\daten\\train.csv\")\n",
    "test.to_csv(r\"C:\\Users\\anika\\Desktop\\daten\\test.csv\")\n",
    "dev.to_csv(r\"C:\\Users\\anika\\Desktop\\daten\\dev.csv\")\n",
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}