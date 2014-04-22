//PyJ2D - Copyright (C) 2011 James Garnon

package pyj2d;

import javax.sound.sampled.AudioFormat;
import java.lang.Byte;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.ShortBuffer;


public class Mixer {

    AudioFormat audioFormat;
    int buffer;
    int sampleByte;
    int sampleMax;
    int sampleMin;
    ByteOrder endian;
    int[] shift;
    double[] data;
    int dataLen;

    /**
     * Mixer combines multiple audio data input to a single output. Can operate
     * with javax.sound.sampled, input obtained from an AudioInputStream and
     * output directed to a SourceDataLine. Supports PCM 16-bit audio format.
     * Argument audioFormat is the AudioFormat of the SourceDataLine, and
     * buffer is the byte size of the ByteArray audio data.
     */
    public Mixer(AudioFormat audioFormat, int buffer) {
        this.audioFormat = audioFormat;
        this.buffer = buffer;
        this.sampleByte = audioFormat.getSampleSizeInBits() == 16 ? 2 : 1;
        this.sampleMax = audioFormat.getSampleSizeInBits() == 16 ? 32767 : 127;
        this.sampleMin = audioFormat.getSampleSizeInBits() == 16 ? -32768 : -128;
        this.endian = !audioFormat.isBigEndian() ? ByteOrder.LITTLE_ENDIAN : ByteOrder.BIG_ENDIAN;
        this.shift = !audioFormat.isBigEndian() ? new int[] {0,8} : new int[] {8,0};
        this.data = new double[this.buffer/this.sampleByte];
        this.dataLen = 0;
        }

    /**
    * Add audio data to the mixer buffer.
    * Argument data is the audio data in a ByteArray, dataLen is the
    * length of data to use, lvolume and rvolume is for L/R volume adjustment
    * of values 0.0 to 1.0.
    */
    public void setAudioData(byte[] data, int dataLen, float lvolume, float rvolume) {
        if (!(lvolume < 1.0) && !(rvolume < 1.0))
            setByteData(data, dataLen);
        else
            setByteData(data, dataLen, lvolume, rvolume);
        if (dataLen > this.dataLen)
            this.dataLen = dataLen;
        }

    /**
    * Add audio data to the mixer buffer.
    * Argument data is the audio data in a ByteArray, dataLen is the
    * length of data to use, volume is for volume adjustment of values
    * 0.0 to 1.0.
    */
    public void setAudioData(byte[] data, int dataLen, float volume) {
        setAudioData(data, dataLen, volume, volume);
        }

    /**
    * Add audio data to the mixer buffer.
    * Argument data is the audio data in a ByteArray, dataLen is the
    * length of data to use.
    */
    public void setAudioData(byte[] data, int dataLen) {
        setByteData(data, dataLen);
        }

    /**
    * Add data to internal array.
    */
    private void setByteData(byte[] data, int dataLen) {
        ShortBuffer dataBuffer = ByteBuffer.wrap(data).order(this.endian).asShortBuffer();
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            this.data[i] += (double) dataBuffer.get(i);
            }
        }

    /**
    * Add data to internal array.
    */
    private void setByteData(byte[] data, int dataLen, float lvolume, float rvolume) {
        ShortBuffer dataBuffer = ByteBuffer.wrap(data).order(this.endian).asShortBuffer();
        for (int i = 0; i < dataLen/this.sampleByte; i+=2) {
            this.data[i] += (double) (dataBuffer.get(i) * lvolume);
            this.data[i+1] += (double) (dataBuffer.get(i+1) * rvolume);
            }
        }

    /**
    * Get mixed audio data.
    * Argument byteArray is a ByteArray the data will be place in.
    * Return data length of ByteArray used.
    */
    public int getAudioData(byte[] byteArray) {
        double samplePeak = checkAudioLevel(this.data, this.dataLen);
        if (samplePeak > this.sampleMax)
            correctAudioLevel(this.data, this.dataLen, samplePeak);
        getByteData(this.data, this.dataLen, byteArray);
        int dataLen = this.dataLen;
        resetMixer();
        return dataLen;
        }

    /**
    * Get mixed data from internal array.
    */
    private void getByteData(double[] data, int dataLen, byte[] byteArray) {
        int pos = 0;
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            byteArray[pos] = (byte) ((int) (data[i])>>this.shift[0] & 0xff);
            byteArray[pos+1] = (byte) ((int) (data[i])>>this.shift[1] & 0xff);
            pos += this.sampleByte;
            }
        }

    /**
    * Check whether audio data level goes over threshold.
    */
    private double checkAudioLevel(double[] data, int dataLen) {
        double xmax = (double) this.sampleMax;
        double xmin = (double) this.sampleMin;
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            if (data[i] > xmax)
                xmax = data[i];
            else if (data[i] < xmin)
                xmin = data[i];
            }
        if (Math.abs(xmin)-1 > xmax)
            xmax = (double) Math.abs(xmin)-1;
        return xmax;
        }

    /**
    * Correct audio data level if exceed threshold.
    */
    private void correctAudioLevel(double[] data, int dataLen, double overflow) {
        float correction = (float) (this.sampleMax/overflow);
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            data[i] = (double) data[i] * correction;
            }
        }

    /**
    * Internal array is zeroed.
    */
    private void resetMixer() {
        for (int i = 0; i < this.dataLen/this.sampleByte; i++) {
            this.data[i] = 0;
            }
        this.dataLen = 0;
        }

    /**
    * Adjust volume of audio data.
    * Argument data is the audio data in a ByteArray, dataLen is the length
    * of data to use, lvolume and rvolume is for L/R volume adjustment
    * of values 0.0 to 1.0.
    * Return input ByteArray adjusted for volume.
    */
    public byte[] processVolume(byte[] data, int dataLen, float lvolume, float rvolume) {
        ShortBuffer dataBuffer = ByteBuffer.wrap(data).order(this.endian).asShortBuffer();
        for (int i = 0; i < dataLen/this.sampleByte; i+=2) {
            dataBuffer.put(i, (short) (dataBuffer.get(i)*lvolume));
            dataBuffer.put(i+1, (short) (dataBuffer.get(i+1)*rvolume));
            }
        return data;
        }

    /**
    * Adjust volume of audio data.
    * Argument data is the audio data in a ByteArray, dataLen is the length
    * of data to use, volume is for volume adjustment of values 0.0 to 1.0.
    * Return input ByteArray adjusted for volume.
    */
    public byte[] processVolume(byte[] data, int dataLen, float volume) {
        byte[] byteArray = processVolume(data, dataLen, volume, volume);
        return byteArray;
        }

    /**
    * Adjust volume of audio data.
    * Argument data is the audio data in a ByteArray, dataLen is the length
    * of data to use.
    * Return input ByteArray adjusted for volume.
    */
    public byte[] processVolume(byte[] data, int dataLen) {
        float volume = (float) 1.0;
        byte[] byteArray = processVolume(data, dataLen, volume, volume);
        return byteArray;
        }

    /**
    * Return mixer data buffer size.
    */
    public int getBufferSize() {
        return this.buffer;
        }

    /**
    * Return AudioFormat of the mixer.
    */
    public AudioFormat getAudioFormat() {
        return this.audioFormat;
        }
    }

