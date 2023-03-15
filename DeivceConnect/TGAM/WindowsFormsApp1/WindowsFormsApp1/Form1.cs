using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using NeuroSky.ThinkGear;
using NeuroSky.ThinkGear.Algorithms;
using DataRow = NeuroSky.ThinkGear.DataRow;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        static Connector connector;
        static bool golfZoneDemo = false;
        static double task_famil_baseline, task_famil_cur, task_famil_change;
        static bool task_famil_first;
        static double mental_eff_baseline, mental_eff_cur, mental_eff_change;
        static bool mental_eff_first;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            connector = new Connector();
            connector.DeviceConnected += new EventHandler(OnDeviceConnected);
            connector.DeviceConnectFail += new EventHandler(OnDeviceFail);
            connector.DeviceValidating += new EventHandler(OnDeviceValidating);
            connector.ConnectScan("COM5");
        }

        private void OnDeviceValidating(object sender, EventArgs e)
        {
            Console.WriteLine("验证该串口设备中...");
        }

        private void OnDeviceFail(object sender, EventArgs e)
        {
            Console.WriteLine("未能查找到EEG设备！：(");
        }

        private void OnDeviceConnected(object sender, EventArgs e)
        {
            Connector.DeviceEventArgs de = (Connector.DeviceEventArgs)e;

            Console.WriteLine("查找到设备串口为： " + de.Device.PortName);

            de.Device.DataReceived += new EventHandler(OnDataReceived);
        }

        static byte rcv_poorSignal_last = 255; // start with impossible value
        static byte rcv_poorSignal;
        static byte rcv_poorSig_cnt = 0;
        static void OnDataReceived(object sender, EventArgs e)
        {
            //Device d = (Device)sender;
            Device.DataEventArgs de = (Device.DataEventArgs)e;
            DataRow[] tempDataRowArray = de.DataRowArray;

            TGParser tgParser = new TGParser();
            tgParser.Read(de.DataRowArray);

            /* Loop through new parsed data */
            for (int i = 0; i < tgParser.ParsedData.Length; i++)
            {
                if (tgParser.ParsedData[i].ContainsKey("MSG_MODEL_IDENTIFIED"))
                {
                    Console.WriteLine("模型识别");


                    connector.setMentalEffortRunContinuous(true);
                    connector.setMentalEffortEnable(true);
                    connector.setTaskFamiliarityRunContinuous(true);
                    connector.setTaskFamiliarityEnable(true);
                    connector.setPositivityEnable(false);
                    //
                    // the following are included to demonstrate the overide messages
                    //
                    connector.setRespirationRateEnable(true); // not allowed with EEG
                    connector.setPositivityEnable(true);// not allowed when famil/diff are enabled
                }
                if (tgParser.ParsedData[i].ContainsKey("MSG_ERR_CFG_OVERRIDE"))
                {
                    Console.WriteLine("ErrorConfigurationOverride: " + tgParser.ParsedData[i]["MSG_ERR_CFG_OVERRIDE"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("MSG_ERR_NOT_PROVISIONED"))
                {
                    Console.WriteLine("ErrorModuleNotProvisioned: " + tgParser.ParsedData[i]["MSG_ERR_NOT_PROVISIONED"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("TimeStamp"))
                {
                    //Console.WriteLine("TimeStamp");
                }
                if (tgParser.ParsedData[i].ContainsKey("Raw"))
                {
                  //  Console.WriteLine("Raw: " + tgParser.ParsedData[i]["Raw"]);

                    FileStream F = new FileStream("TGMARaw.txt", FileMode.Append, FileAccess.Write);
                    StreamWriter writer = new StreamWriter(F);
                    TextWriter oldOut = Console.Out;
                    Console.SetOut(writer);
                    Console.WriteLine(tgParser.ParsedData[i]["Raw"]);
                    Console.SetOut(oldOut);
                    writer.Close();
                    F.Close();
                }
                if (tgParser.ParsedData[i].ContainsKey("RespiratoryRate"))
                {
                    Console.WriteLine("RespiratoryRate: " + tgParser.ParsedData[i]["RespiratoryRate"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("RawCh1"))
                {
                    //Console.WriteLine("RawCh1: " + tgParser.ParsedData[i]["RawCh1"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("RawCh2"))
                {
                    //Console.Write(", Raw Ch2:" + tgParser.ParsedData[i]["RawCh2"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("PoorSignal"))
                {
                    // NOTE: this doesn't work well with BMD sensors Dual Headband or CardioChip

                    rcv_poorSignal = (byte)tgParser.ParsedData[i]["PoorSignal"];
                    if (rcv_poorSignal != rcv_poorSignal_last || rcv_poorSig_cnt >= 30)
                    {
                        // when there is a change of state OR every 30 reports
                        rcv_poorSig_cnt = 0; // reset counter
                        rcv_poorSignal_last = rcv_poorSignal;
                        if (rcv_poorSignal == 0)
                        {
                            // signal is good, we are connected to a subject
                            Console.WriteLine("信号值: 电极接触良好，您已正确佩戴设备");
                        }
                        else
                        {
                            Console.WriteLine("信号值: " + rcv_poorSignal);
                        }
                    }
                    else rcv_poorSig_cnt++;
                }
                if (tgParser.ParsedData[i].ContainsKey("Attention"))
                {
                    if (tgParser.ParsedData[i]["Attention"] != 0) Console.WriteLine("专注度： " + tgParser.ParsedData[i]["Attention"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("Attention 1"))
                {
                    if (tgParser.ParsedData[i]["Attention 1"] != 0) Console.WriteLine("专注度 1： " + tgParser.ParsedData[i]["Attention 1"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("Attention 2"))
                {
                    if (tgParser.ParsedData[i]["Attention 2"] != 0) Console.WriteLine("专注度 2： " + tgParser.ParsedData[i]["Attention 2"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("Meditation"))
                {
                    if (tgParser.ParsedData[i]["Meditation"] != 0) Console.WriteLine("放松度： " + tgParser.ParsedData[i]["Meditation"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("Meditation 1"))
                {
                    if (tgParser.ParsedData[i]["Meditation 1"] != 0) Console.WriteLine("放松度 1： " + tgParser.ParsedData[i]["Meditation 1"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("Meditation 2"))
                {
                    if (tgParser.ParsedData[i]["Meditation 2"] != 0) Console.WriteLine("放松度 2： " + tgParser.ParsedData[i]["Meditation 2"]);
                }
                if (tgParser.ParsedData[i].ContainsKey("BlinkStrength"))
                {
                    Console.WriteLine("\t\t眨眼强度放松度 " + tgParser.ParsedData[i]["BlinkStrength"]);
                }

                if (tgParser.ParsedData[i].ContainsKey("MentalEffort"))
                {
                    mental_eff_cur = (Double)tgParser.ParsedData[i]["MentalEffort"];
                    if (mental_eff_first)
                    {
                        mental_eff_first = false;
                    }
                    else
                    {
                        /*
                         * calculate the percentage change from the previous sample
                         */
                        mental_eff_change = calcPercentChange(mental_eff_baseline, mental_eff_cur);
                        if (mental_eff_change > 500.0 || mental_eff_change < -500.0)
                        {
                            Console.WriteLine("\t\t脑力劳动：超出范围");
                        }
                        else
                        {
                            Console.WriteLine("\t\t脑力劳动： " + mental_eff_change + " %");
                        }
                    }
                    mental_eff_baseline = mental_eff_cur;
                }

                if (tgParser.ParsedData[i].ContainsKey("TaskFamiliarity"))
                {
                    task_famil_cur = (Double)tgParser.ParsedData[i]["TaskFamiliarity"];
                    if (task_famil_first)
                    {
                        task_famil_first = false;
                    }
                    else
                    {
                        /*
                         * calculate the percentage change from the previous sample
                         */
                        task_famil_change = calcPercentChange(task_famil_baseline, task_famil_cur);
                        if (task_famil_change > 500.0 || task_famil_change < -500.0)
                        {
                            Console.WriteLine("\t\t任务熟悉度：超出范围");
                        }
                        else
                        {
                            Console.WriteLine("\t\t任务熟悉度： " + task_famil_change + " %");
                        }
                    }
                    task_famil_baseline = task_famil_cur;
                }

                if (tgParser.ParsedData[i].ContainsKey("Positivity"))
                {
                    Console.WriteLine("\t\t积极性: " + tgParser.ParsedData[i]["Positivity"]);
                }
            }
        }

        static double calcPercentChange(double baseline, double current)
        {
            double change;

            if (baseline == 0.0) baseline = 1.0; //don't allow divide by zero
            /*
             * calculate the percentage change
             */
            change = current - baseline;
            change = (change / baseline) * 1000.0 + 0.5;
            change = Math.Floor(change) / 10.0;
            return (change);
        }

    }
}
